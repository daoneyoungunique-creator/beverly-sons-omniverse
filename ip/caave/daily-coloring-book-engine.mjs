// CAAVE Daily Coloring Book Engine — pure draft-planning logic.
// No image generation, publishing, minting or checkout side effects.
export const SUPREME_MATH = Object.freeze(["CIPHER","KNOWLEDGE","WISDOM","UNDERSTANDING","CULTURE","POWER","EQUALITY","GOD","BUILD","BORN"]);
export const PAGES_PER_BOOK = 12;
export function digitRoot(n) {
  if (!Number.isSafeInteger(n) || n < 1) throw new RangeError("Number must be a positive safe integer");
  let digits = String(n).split("").map(Number);
  let sum = digits.reduce((a,b)=>a+b,0);
  while (sum > 9) sum = String(sum).split("").reduce((a,b)=>a+Number(b),0);
  return {digits, root:sum, word:SUPREME_MATH[sum]};
}
export function pageForNumber(n) {
  if (!Number.isSafeInteger(n) || n < 1) throw new RangeError("Number must be a positive safe integer");
  return {number:n,bookNumber:Math.floor((n-1)/PAGES_PER_BOOK)+1,pageNumber:((n-1)%PAGES_PER_BOOK)+1};
}
export function bookRange(bookNumber) {
  if (!Number.isSafeInteger(bookNumber) || bookNumber < 1) throw new RangeError("Book must be a positive safe integer");
  const first=(bookNumber-1)*PAGES_PER_BOOK+1;
  return {bookNumber,first,last:first+PAGES_PER_BOOK-1};
}
export function createDailyColoringDraft(n, {character="CAAVE Guardian", series="CAAVE Supreme Math Coloring Adventures"}={}) {
  const location=pageForNumber(n), math=digitRoot(n);
  return {
    id:`CAAVE-COLOR-${String(n).padStart(5,"0")}`,
    series,character,...location,
    supremeMath:math,
    status:"DRAFT",
    approved:false,
    artworkReady:false,
    published:false,
    artPrompt:`Original printable coloring-book line art for ${series}, sequential number ${n}, Book ${location.bookNumber}, page ${location.pageNumber} of 12. Feature ${character} wearing BEVERLY & SONS × CAAVE × UNITED CONDITIONING apparel, exploring the theme ${math.word}. Bold clean black outlines on pure white, open spaces to color, expressive kid-friendly action, consistent character design, no gradients, no gray fills, no photographic texture, no watermark. Print-ready portrait composition with safe margins. Include one clear outlined numeral ${n} as a coloring element. Create original art, not a copy of third-party artwork.`,
    lessonPrompt:`Teach number ${n} as ${math.digits.join(" + ")} = ${math.root} (${math.word}); give one age-appropriate action, one affirmation, and a guardian story moment.`,
    assetRequirements:{colorMode:"black-and-white",pageCountPerBook:PAGES_PER_BOOK,doubleSided:true,bleed:"set at layout stage",output:"digital PDF"},
    nextActions:["generate original line art","check character consistency and print legibility","place into numbered book layout","review and approve","export digital PDF"]
  };
}
export function createBookDraft(bookNumber,options={}) {
  const range=bookRange(bookNumber);
  return {...range,title:`CAAVE Supreme Math Coloring Adventures — Book ${bookNumber}`,status:"DRAFT",pages:Array.from({length:PAGES_PER_BOOK},(_,i)=>createDailyColoringDraft(range.first+i,options))};
}
