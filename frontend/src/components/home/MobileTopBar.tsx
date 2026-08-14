import { useState } from "react";
import { Menu, Sparkles } from "lucide-react";
import { Sheet, SheetContent, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { SidebarInner } from "@/components/home/Sidebar";
import { mobileTopBarStyles as s } from "@/styles/home/sidebar.styles";

export function MobileTopBar() {
  const [open, setOpen] = useState(false);

  return (
    <div className={s.bar}>
      <Sheet open={open} onOpenChange={setOpen}>
        <SheetTrigger asChild>
          <button type="button" className={s.trigger} aria-label="Open menu">
            <Menu className={s.triggerIcon} />
          </button>
        </SheetTrigger>
        <SheetContent side="left" className={s.sheetContent}>
          <SheetTitle className="sr-only">Navigation</SheetTitle>
          <SidebarInner onNavigate={() => setOpen(false)} />
        </SheetContent>
      </Sheet>

      <div className={s.brand}>
        <div className={s.brandBadge} style={{ background: "var(--gradient-primary)" }}>
          <Sparkles className={s.brandBadgeIcon} />
        </div>
        <span className={s.brandText}>Smart Content AI</span>
      </div>

      {/* spacer to balance the hamburger so brand stays centered */}
      <span className={s.spacer} aria-hidden />
    </div>
  );
}
