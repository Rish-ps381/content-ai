import { createFileRoute } from "@tanstack/react-router";
import { Content } from "@/components/home/Content";

export const Route = createFileRoute("/home/create")({
  component: Content,
});
