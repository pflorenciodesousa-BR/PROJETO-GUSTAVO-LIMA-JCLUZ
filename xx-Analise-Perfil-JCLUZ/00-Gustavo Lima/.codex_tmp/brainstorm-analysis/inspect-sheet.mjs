import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = process.argv[2];
const input = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(input);
const sheet = workbook.worksheets.getItem("Postagens 2026");
const range = sheet.getRange("A1850:P2310");
const values = range.values;

const toDate = (serial) => new Date(Date.UTC(1899, 11, 30) + serial * 86400000);
const mean = (items) => items.length ? items.reduce((sum, item) => sum + item, 0) / items.length : null;
const categoryOf = (title, type) => {
  const value = `${title} ${type}`.toLowerCase();
  if (value.includes("cotação") || value.includes("cotacao") || value.includes("quadro")) return "cotacao";
  if (value.includes("carrossel")) return "carrossel";
  if (value.includes("frase")) return "frase";
  if (value.includes("foto")) return "foto";
  return "espontaneo";
};

const posts = [];
for (let i = 0; i < values.length; i += 1) {
  const row = values[i];
  if (typeof row[0] !== "string" || typeof row[1] !== "string" || typeof row[2] !== "number" || !String(row[3]).startsWith("24h")) continue;
  if (row[0] === "##" || row[0] === "ANÚNCIO") continue;
  const phases = values.slice(i, i + 4).map((phase, phaseIndex) => ({
    phase: ["24h", "1w", "2w", "3w"][phaseIndex],
    views: typeof phase[4] === "number" ? phase[4] : null,
    reach: typeof phase[5] === "number" ? phase[5] : null,
    retention: typeof phase[6] === "number" ? phase[6] : null,
    hook: typeof phase[7] === "number" ? phase[7] : null,
    likes: typeof phase[8] === "number" ? phase[8] : null,
    shares: typeof phase[10] === "number" ? phase[10] : null,
    comments: typeof phase[12] === "number" ? phase[12] : null,
    saves: typeof phase[13] === "number" ? phase[13] : null,
    follows: typeof phase[14] === "number" ? phase[14] : null,
  }));
  const date = toDate(row[2]);
  posts.push({
    row: 1850 + i,
    title: row[0].trim(),
    type: row[1].trim(),
    category: categoryOf(row[0], row[1]),
    date: date.toISOString().slice(0, 10),
    weekday: ["domingo", "segunda", "terça", "quarta", "quinta", "sexta", "sábado"][date.getUTCDay()],
    slot: String(row[3]).includes("dia") ? "dia" : "noite",
    note: row[15] || null,
    phases,
  });
}

const aggregate = (items) => ({
  posts: items.length,
  views24h: mean(items.map((post) => post.phases[0].views).filter(Number.isFinite)),
  reach24h: mean(items.map((post) => post.phases[0].reach).filter(Number.isFinite)),
  retention24h: mean(items.map((post) => post.phases[0].retention).filter(Number.isFinite)),
  hook24h: mean(items.map((post) => post.phases[0].hook).filter(Number.isFinite)),
  interactions24h: mean(items.map((post) => {
    const p = post.phases[0];
    return (p.likes || 0) + (p.shares || 0) + (p.comments || 0) + (p.saves || 0);
  })),
  growth1w: mean(items.map((post) => post.phases[1].views && post.phases[0].views ? post.phases[1].views / post.phases[0].views - 1 : null).filter(Number.isFinite)),
  growth2wFrom1w: mean(items.map((post) => post.phases[2].views && post.phases[1].views ? post.phases[2].views / post.phases[1].views - 1 : null).filter(Number.isFinite)),
  samples1w: items.filter((post) => Number.isFinite(post.phases[1].views)).length,
  samples2w: items.filter((post) => Number.isFinite(post.phases[2].views)).length,
  samples3w: items.filter((post) => Number.isFinite(post.phases[3].views)).length,
});

const categories = Object.fromEntries([...new Set(posts.map((post) => post.category))].map((category) => [category, aggregate(posts.filter((post) => post.category === category))]));
const weekdays = Object.fromEntries([...new Set(posts.map((post) => post.weekday))].map((weekday) => [weekday, aggregate(posts.filter((post) => post.weekday === weekday))]));
const slots = Object.fromEntries(["dia", "noite"].map((slot) => [slot, aggregate(posts.filter((post) => post.slot === slot))]));
const quotations = posts.filter((post) => post.category === "cotacao");

console.log(JSON.stringify({
  sheets: workbook.worksheets.items.map((item) => item.name),
  posts,
  categories,
  weekdays,
  slots,
  quotationSummary: aggregate(quotations),
}));
