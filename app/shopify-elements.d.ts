import type { AnchorHTMLAttributes, HTMLAttributes } from "react";

declare global {
  namespace JSX {
    interface IntrinsicElements {
      "s-app-nav": HTMLAttributes<HTMLElement>;
      "s-link": AnchorHTMLAttributes<HTMLAnchorElement>;
    }
  }
}

export {};
