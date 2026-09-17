import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const inputPath = process.argv[2];
if (!inputPath) {
  throw new Error("Missing workbook path");
}

const input = await FileBlob.load(inputPath);
const workbook = await SpreadsheetFile.importXlsx(input);
const overview = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 8000,
  tableMaxRows: 8,
  tableMaxCols: 12,
  tableMaxCellChars: 120,
});

const sheet = workbook.worksheets.getItem("Postagens 2026");
const requestedRange = process.argv[3];
if (requestedRange) {
  const target = sheet.getRange(requestedRange);
  console.log(JSON.stringify({
    sheet: "Postagens 2026",
    range: requestedRange,
    values: target.values,
    formulas: target.formulas,
  }, null, 2));
  process.exit(0);
}
const used = sheet.getUsedRange(true);
const values = used ? used.values : [];

const months = new Set([
  "JANEIRO", "FEVEREIRO", "MARÇO", "ABRIL", "MAIO", "JUNHO",
  "JULHO", "AGOSTO", "SETEMBRO", "OUTUBRO", "NOVEMBRO", "DEZEMBRO",
]);
const monthMarkers = values
  .map((row, index) => ({ row: index + 1, label: row[0] }))
  .filter(({ label }) => typeof label === "string" && months.has(label.trim().toUpperCase()));
const augustMarker = monthMarkers.find(({ label }) => label.trim().toUpperCase() === "AGOSTO");
const nextMarker = monthMarkers.find(({ row }) => augustMarker && row > augustMarker.row);
const augustStart = augustMarker ? augustMarker.row - 1 : 0;
const augustEnd = nextMarker ? nextMarker.row - 1 : values.length;
const augustRows = values
  .slice(augustStart, augustEnd)
  .map((cells, offset) => ({ row: augustStart + offset + 1, cells }))
  .filter(({ cells }) => cells.some((cell) => cell !== null && cell !== ""));

const excelDate = (serial) => {
  if (typeof serial !== "number") return null;
  const epoch = Date.UTC(1899, 11, 30);
  return new Date(epoch + Math.floor(serial) * 86400000).toISOString().slice(0, 10);
};
const isPostName = (name) => {
  if (typeof name !== "string" || !name.trim()) return false;
  const normalized = name.trim().toUpperCase();
  return !months.has(normalized)
    && !/^SEMANA\s+\d+/.test(normalized)
    && normalized !== "ANÚNCIO"
    && !/^#+$/.test(normalized);
};
const snapshotFrom = (cells, row) => ({
  row,
  period: typeof cells[2] === "number" ? cells[3] : cells[2],
  analysisDate: typeof cells[3] === "number" ? excelDate(cells[3]) : null,
  views: cells[4],
  reach: cells[5],
  retention: cells[6],
  threeSecondRate: cells[7],
  likes: cells[8],
  likesRate: cells[9],
  shares: cells[10],
  sharesRate: cells[11],
  comments: cells[12],
  saves: cells[13],
  followers: cells[14],
  intuitiveAnalysis: cells[15],
});

const posts = [];
let currentPost = null;
for (let index = augustStart; index < augustEnd; index += 1) {
  const cells = values[index];
  const name = cells[0];
  if (!isPostName(name)) continue;

  if (typeof cells[2] === "number") {
    currentPost = {
      name: name.trim(),
      type: cells[1],
      datePost: excelDate(cells[2]),
      rowStart: index + 1,
      timeSlot: typeof cells[3] === "string" ? cells[3] : null,
      snapshots: [],
    };
    posts.push(currentPost);
  }

  if (currentPost && currentPost.name === name.trim()) {
    const snapshot = snapshotFrom(cells, index + 1);
    if ([snapshot.views, snapshot.reach, snapshot.likes, snapshot.shares, snapshot.comments, snapshot.saves]
      .some((value) => typeof value === "number")) {
      currentPost.snapshots.push(snapshot);
    }
  }
}

const compactPosts = posts.map((post) => ({
  name: post.name,
  type: post.type,
  datePost: post.datePost,
  rowStart: post.rowStart,
  timeSlot: post.timeSlot,
  snapshots: post.snapshots,
  latest: post.snapshots.at(-1) ?? null,
}));

const filledThrough = compactPosts
  .map(({ datePost }) => datePost)
  .filter(Boolean)
  .sort()
  .at(-1) ?? null;

const compactSnapshot = (snapshot) => snapshot ? {
  period: snapshot.period,
  analysisDate: snapshot.analysisDate,
  views: snapshot.views,
  reach: snapshot.reach,
  retention: snapshot.retention,
  threeSecondRate: snapshot.threeSecondRate,
  likes: snapshot.likes,
  likesRate: snapshot.likesRate,
  shares: snapshot.shares,
  sharesRate: snapshot.sharesRate,
  comments: snapshot.comments,
  saves: snapshot.saves,
  followers: snapshot.followers,
} : null;

const indexPosts = compactPosts.map((post) => ({
  row: post.rowStart,
  datePost: post.datePost,
  name: post.name,
  type: post.type,
  timeSlot: post.timeSlot,
  snapshotCount: post.snapshots.length,
  baseline: compactSnapshot(post.snapshots[0]),
  latest: compactSnapshot(post.latest),
}));

console.log(JSON.stringify({
  sheet: "Postagens 2026",
  rowCount: values.length,
  columnCount: values[0]?.length ?? 0,
  headers: values[0],
  augustRange: `A${augustStart + 1}:P${augustEnd}`,
  filledThrough,
  postCount: indexPosts.length,
  posts: indexPosts,
}, null, 2));
