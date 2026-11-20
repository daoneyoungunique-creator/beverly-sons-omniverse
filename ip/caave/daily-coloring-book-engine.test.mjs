import test from "node:test";import assert from "node:assert/strict";
import {digitRoot,pageForNumber,bookRange,createBookDraft,createDailyColoringDraft} from "./daily-coloring-book-engine.mjs";
test("continuous numbering across books",()=>{assert.deepEqual(pageForNumber(12),{number:12,bookNumber:1,pageNumber:12});assert.deepEqual(pageForNumber(13),{number:13,bookNumber:2,pageNumber:1});assert.deepEqual(bookRange(100),{bookNumber:100,first:1189,last:1200});});
test("supreme mathematics key",()=>{assert.equal(digitRoot(114).root,6);assert.equal(digitRoot(114).word,"EQUALITY");assert.equal(digitRoot(147).root,3);});
test("twelve pages and draft-only",()=>{const b=createBookDraft(2);assert.equal(b.pages.length,12);assert.equal(b.pages[0].number,13);assert.equal(b.pages[11].number,24);assert.ok(b.pages.every(p=>p.status==="DRAFT"&&!p.published&&!p.approved&&!p.artworkReady));});
test("no zero or negative numbers",()=>{assert.throws(()=>pageForNumber(0),RangeError);assert.throws(()=>digitRoot(-1),RangeError);});
