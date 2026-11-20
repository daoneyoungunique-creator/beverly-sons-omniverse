/** CAAVE Daily Media Engine — source-derived, deterministic core.
 * Draft generation only; no network requests or publishing actions.
 */
export const SUPREME_MATH = Object.freeze({
  0:{word:"CIPHER",essence:"Whole, circle, completion"},
  1:{word:"KNOWLEDGE",essence:"Awareness, observation, foundation"},
  2:{word:"WISDOM",essence:"Action, values made visible"},
  3:{word:"UNDERSTANDING",essence:"Connection, cause to effect"},
  4:{word:"CULTURE",essence:"Way of life, structure, identity"},
  5:{word:"POWER",essence:"Refinement, sharpening the blade"},
  6:{word:"EQUALITY",essence:"Balance, proper weight, harmony"},
  7:{word:"GOD",essence:"Leadership, accountable sovereignty"},
  8:{word:"BUILD",essence:"Creation from destruction"},
  9:{word:"BORN",essence:"New beginnings, resistance broken"},
});
export const STAGES = Object.freeze([
 "DAILY NUMBER","SUPREME MATH","TEACHING EXTRACTION","SCENE GENERATOR",
 "AI IMAGE BRIEF","DEPTH+PARALLAX","MUSIC ANALYSIS","BEAT SYNC",
 "SHORTS EXTRACTION","NFT METADATA","CURRICULUM MODULE","AUTO PUBLISH"
]);
export function computeKey(value){
 const raw=String(value).trim();
 if(!/^\d{1,12}$/.test(raw)) throw new Error("Daily key must contain 1–12 digits");
 const digits=[...raw].map(Number);
 let sum=digits.reduce((a,b)=>a+b,0);
 while(sum>9) sum=[...String(sum)].reduce((a,b)=>a+Number(b),0);
 return {raw,digits,sum,meanings:digits.map(d=>SUPREME_MATH[d]),
   result:SUPREME_MATH[sum]};
}
export function createDraftPipeline(value,sourceIp="CAAVE"){
 const key=computeKey(value);
 return {key,sourceIp,approvalStatus:"DRAFT",published:false,minted:false,
  stages:STAGES.map((label,i)=>({number:i+1,label,status:"PENDING_REVIEW",content:null}))};
}
export function validatePipeline(p){
 const errors=[];
 if(!p||!Array.isArray(p.stages)||p.stages.length!==12) errors.push("Exactly 12 stages required");
 else p.stages.forEach((s,i)=>{
   if(s.number!==i+1||s.label!==STAGES[i]) errors.push("Stage mismatch at "+(i+1));
   if(typeof s.content!=="string"||!s.content.trim()) errors.push("Missing content at "+(i+1));
 });
 return {valid:errors.length===0,errors};
}
