import { Outlet, createFileRoute, redirect } from "@tanstack/react-router";
import { Sidebar } from "@/components/home/Sidebar";
import { MobileTopBar } from "@/components/home/MobileTopBar";
import { homeLayoutStyles as s } from "@/styles/home/layout.styles";

export const Route = createFileRoute("/home")({
  head: () => ({
    meta: [
      { title: "Smart Content AI — Stella Apps" },
      {
        name: "description",
        content: "Create professional, on-brand content in seconds with Smart Content AI.",
      },
    ],
  }),
  beforeLoad: ({ location }) => {
    if (location.pathname === "/home" || location.pathname === "/home/") {
      throw redirect({ to: "/home/create" });
    }
  },
  component: HomeLayout,
});

function HomeLayout() {
  return (
    <div className={s.shell}>
      <Sidebar />
      <div className={s.body}>
        <MobileTopBar />
        <main className={s.main}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
