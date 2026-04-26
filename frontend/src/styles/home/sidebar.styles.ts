export const sidebarStyles = {
  // Desktop sidebar visible from lg+; below that we use the mobile drawer.
  aside:
    "hidden lg:flex h-screen w-72 shrink-0 flex-col border-r border-border bg-sidebar",
  // Drawer variant — fills the Sheet, no fixed height/border (Sheet handles that).
  drawer: "flex h-full w-full flex-col bg-sidebar",
  createWrap: "px-3 pb-2",
  createBtn:
    "flex items-center justify-center gap-2 rounded-xl px-3 py-2.5 text-sm font-medium text-primary-foreground shadow-elegant transition-all hover:opacity-90",
  createBtnActive: "ring-2 ring-ring ring-offset-2 ring-offset-background",
  icon: "h-4 w-4",
} as const;

export const mobileTopBarStyles = {
  bar: "lg:hidden sticky top-0 z-30 flex items-center justify-between gap-3 border-b border-border bg-background/80 px-4 py-3 backdrop-blur",
  trigger:
    "inline-flex h-10 w-10 items-center justify-center rounded-lg border border-border bg-card text-foreground transition-colors hover:bg-accent",
  triggerIcon: "h-5 w-5",
  brand: "flex items-center gap-2",
  brandBadge:
    "flex h-8 w-8 items-center justify-center rounded-lg text-primary-foreground shadow-soft",
  brandBadgeIcon: "h-4 w-4",
  brandText: "text-sm font-semibold text-foreground",
  spacer: "h-10 w-10",
  sheetContent: "p-0 w-72 sm:w-80",
} as const;
