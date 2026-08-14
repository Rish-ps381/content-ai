export const contentStyles = {
  page: "min-h-full px-4 py-8 sm:px-8 sm:py-12",
  container: "mx-auto w-full max-w-4xl",

  header: "mb-8 text-center",
  title:
    "bg-clip-text text-4xl font-extrabold tracking-tight text-transparent sm:text-5xl",
  subtitle: "mt-3 text-base text-muted-foreground sm:text-lg",
  actionsRow: "mt-6 flex flex-wrap items-center justify-center gap-3",
  actionBtn:
    "inline-flex items-center gap-2 rounded-xl border border-border bg-card px-4 py-2.5 text-sm font-medium text-foreground shadow-soft transition-all hover:bg-accent",
  actionIcon: "h-4 w-4",

  card: "rounded-2xl border border-border bg-card p-6 shadow-elegant sm:p-8",
  cardHead: "mb-6 flex items-center gap-2",
  cardHeadIcon: "h-5 w-5 text-primary",
  cardHeadTitle: "text-lg font-semibold text-foreground",

  grid: "grid gap-5 sm:grid-cols-2",
  full: "sm:col-span-2",
  selectTrigger: "h-11 rounded-lg border-border bg-background",

  generateBtn:
    "mt-7 inline-flex w-full items-center justify-center gap-2 rounded-xl px-6 py-3.5 text-base font-semibold text-primary-foreground shadow-elegant transition-transform hover:-translate-y-0.5",
  generateIcon: "h-5 w-5",

  fieldLabel: "mb-1.5 block text-sm font-medium text-foreground",
  fieldLabelStar: "text-primary",
} as const;
