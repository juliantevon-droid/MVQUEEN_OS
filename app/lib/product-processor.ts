import prisma from "../db.server";
import { unauthenticated } from "../shopify.server";
import { generateCatalogPackage, type ProductSnapshot } from "./mvqueen-intelligence";

const PRODUCT_QUERY = \`#graphql
query MVQueenProduct($id: ID!) {
  product(id: $id) {
    id title descriptionHtml productType vendor tags
    media(first: 100) { nodes { id alt } }
  }
}\`;

const PRODUCT_UPDATE = \`#graphql
mutation MVQueenProductUpdate($product: ProductUpdateInput!) {
  productUpdate(product: $product) {
    product { id title productType updatedAt }
    userErrors { field message }
  }
}\`;

const FILE_UPDATE = \`#graphql
mutation MVQueenFileAlt($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) {
    files { id }
    userErrors { field message }
  }
}\`;

export async function processProductJob(jobId: string) {
  const job = await prisma.productJob.findUnique({ where: { id: jobId } });
  if (!job) throw new Error("Product job not found");
  await prisma.productJob.update({ where: { id: jobId },
    data: { status:"processing", attempts:{increment:1}, startedAt:new Date(), error:null } });

  try {
    const { admin } = await unauthenticated.admin(job.shop);
    const response = await admin.graphql(PRODUCT_QUERY, { variables:{id:job.productGid} });
    const body = await response.json();
    const product: ProductSnapshot | null = body.data?.product ?? null;
    if (!product) throw new Error("Shopify product not found");

    const pkg = generateCatalogPackage(product);
    const metafields = [
      {namespace:"classification",key:"department",type:"single_line_text_field",value:pkg.c.department},
      {namespace:"classification",key:"family",type:"single_line_text_field",value:pkg.c.family},
      {namespace:"classification",key:"subcollection",type:"single_line_text_field",value:pkg.c.subcollection},
      {namespace:"classification",key:"style",type:"single_line_text_field",value:"MVQueen Edit"},
      ...(pkg.attributes.material ? [{namespace:"attributes",key:"material",type:"single_line_text_field",value:pkg.attributes.material}] : []),
      ...(pkg.attributes.color ? [{namespace:"attributes",key:"color",type:"single_line_text_field",value:pkg.attributes.color}] : []),
      ...(pkg.attributes.fit ? [{namespace:"attributes",key:"fit",type:"single_line_text_field",value:pkg.attributes.fit}] : []),
      ...(pkg.attributes.occasion ? [{namespace:"attributes",key:"occasion",type:"single_line_text_field",value:pkg.attributes.occasion}] : []),
      {namespace:"catalog",key:"short_description",type:"single_line_text_field",value:pkg.shortDescription},
      {namespace:"catalog",key:"seo_keywords",type:"list.single_line_text_field",value:JSON.stringify(pkg.keywords)},
      {namespace:"catalog",key:"classification_confidence",type:"single_line_text_field",value:pkg.c.confidence},
      {namespace:"catalog",key:"review_status",type:"single_line_text_field",value:pkg.c.confidence === "review" ? "needs_review" : "ready"}
    ];

    const update = await admin.graphql(PRODUCT_UPDATE, { variables:{ product:{
      id:product.id,
      title: pkg.title !== product.title ? pkg.title : product.title,
      descriptionHtml: pkg.descriptionHtml,
      productType: product.productType?.trim() ? product.productType : pkg.c.productType,
      tags:pkg.tags,
      seo:{title:pkg.seoTitle,description:pkg.seoDescription}, metafields
    }}});
    const updateBody = await update.json();
    const errors = updateBody.data?.productUpdate?.userErrors ?? [];
    if (errors.length) throw new Error(errors.map((e:{message:string})=>e.message).join("; "));

    const media = (product.media ?? []).filter(m => m.id && !m.alt);
    if (media.length) await admin.graphql(FILE_UPDATE, {
      variables:{files:media.map(m=>({id:m.id,alt:\`\${pkg.title} | MVQueen\`}))}
    });

    const updatedAt = updateBody.data?.productUpdate?.product?.updatedAt;
    if (!updatedAt) throw new Error("Shopify product update did not return updatedAt");
    await prisma.productAutomationState.upsert({
      where: { shop_productGid: { shop: job.shop, productGid: product.id } },
      update: { lastAutomationUpdatedAt: new Date(updatedAt), automationVersion: "1" },
      create: { shop: job.shop, productGid: product.id, lastAutomationUpdatedAt: new Date(updatedAt), automationVersion: "1" },
    });

    await prisma.productJob.update({where:{id:jobId},data:{status:"completed",completedAt:new Date()}});
  } catch (error) {
    await prisma.productJob.update({where:{id:jobId},data:{
      status:"failed",error:error instanceof Error ? error.message : String(error)
    }});
    throw error;
  }
}
