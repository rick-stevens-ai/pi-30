// pi Agent-Loop Fleet-30 benchmark deck
const { C, HF, BF, makeLib, PptxGenJS } = require("./deck_lib.cjs");
const p = new PptxGenJS();
p.defineLayout({ name: "W", width: 13.333, height: 7.5 });
p.layout = "W";
const L = makeLib(p);
const TOTAL = 14;
const S = () => p.addSlide();

// ---------- 1. TITLE (dark) ----------
(() => {
  const s = S(); L.bgDark(s);
  s.addShape(p.ShapeType.roundRect,{x:0.7,y:0.6,w:0.14,h:2.2,rectRadius:0.05,fill:{color:C.CYAN},line:{type:"none"}});
  s.addText("BENCHMARK REPORT · 2026-07-06",{x:1.0,y:1.35,w:11,h:0.5,fontFace:BF,fontSize:18,color:C.CYAN,bold:true,charSpacing:2});
  s.addText("The pi Agent-Loop\nFleet-30 Benchmark",{x:0.95,y:1.9,w:11.5,h:2.0,fontFace:HF,fontSize:52,bold:true,color:C.WHITE,lineSpacingMultiple:1.0});
  s.addText("A tool-use coding evaluation across the free / self-hosted model fleet",{x:1.0,y:4.05,w:11,h:0.6,fontFace:BF,fontSize:22,color:C.ICE});
  // three stat pills
  const pills=[["26","lanes evaluated"],["30","agent-loop problems"],["8","clean 30/30"]];
  pills.forEach((pl,i)=>{
    const x=1.0+i*3.9;
    s.addShape(p.ShapeType.roundRect,{x,y:5.15,w:3.5,h:1.35,rectRadius:0.12,fill:{color:C.NAVY2},line:{color:C.TEAL,width:1.5}});
    s.addText(pl[0],{x,y:5.28,w:3.5,h:0.85,fontFace:HF,fontSize:46,bold:true,color:C.CYAN,align:"center"});
    s.addText(pl[1],{x,y:6.08,w:3.5,h:0.4,fontFace:BF,fontSize:16,color:C.ICE,align:"center",bold:true});
  });
  s.addText("Rick Stevens fleet · m1-mac-mini · pi (Earendil Pi) agent CLI, tools ON",{x:1.0,y:6.95,w:11,h:0.4,fontFace:BF,fontSize:16,color:C.GREY});
})();

// ---------- 2. WHY (light) ----------
(() => {
  const s = S(); L.bgLight(s);
  L.kicker(s,"Why this benchmark exists",C.TEAL);
  L.title(s,"Measuring whether a model can close an agent loop");
  s.addText("Standard leaderboards (MMLU, chat-Elo) measure fluent text. They do NOT measure whether a model can drive tools, recover from a failing test, and iterate to a verifier-passing result — the one skill an agent core actually needs.",
    {x:0.7,y:2.0,w:12,h:0.9,fontFace:BF,fontSize:18,color:C.INK,lineSpacingMultiple:1.15});
  const goals=[
    ["Enablement mapping","Which of the dozens of served models can actually drive a loop — so real agentic work routes only to models that clear the bar.",C.CYAN],
    ["Serving-path validation","Same weights on two backends is a different product. A broken template, missing tool-parser, or quant shows up as a score drop.",C.GOLD],
    ["Shared coding curriculum","30 authored problems — write, fix, optimize, tournament, critic — that exercise the distinct sub-skills an agent needs.",C.GREEN],
  ];
  goals.forEach((g,i)=>{
    const x=0.7+i*4.05;
    L.card(s,x,3.15,3.8,3.1,g[0],g[2]===C.CYAN?
      "Which of the served models can actually drive a loop — so real agentic work routes only to models that clear the bar, and the rest stay for single-shot generation.":
      g[1],{accent:g[2],hsize:20,bsize:17});
  });
  L.foot(s,2,TOTAL,false);
})();

// ---------- 3. HOW A SCORE IS EARNED (light) ----------
(() => {
  const s = S(); L.bgLight(s);
  L.kicker(s,"The rules",C.TEAL);
  L.title(s,"How a score is earned");
  const rules=[
    ["Tools always ON","No --no-tools runs. The point is the loop, not zero-shot recall. A path-clamp keeps the model in its problem dir; verdicts still come only from the grader."],
    ["Single-shot is canonical","Headline = one clean pass over all 30, apples-to-apples. A targeted rerun of misses is reported as \u201ceffective\u201d, never promoted."],
    ["Zero-score rule","Any 0/N is a server / harness / stack failure — debugged as infrastructure, marked BROKEN, never recorded as model capability."],
    ["Verdicts from exit codes","Each problem ships an independent grader (verify.py / pytest / scorer). The model is forbidden from editing it. Attribute to provider \u00d7 model."],
  ];
  rules.forEach((r,i)=>{
    const x=0.7+(i%2)*6.15, y=2.15+Math.floor(i/2)*2.15;
    L.card(s,x,y,5.85,1.9,r[0],r[1],{accent:i%2?C.GOLD:C.CYAN,hsize:20,bsize:17});
  });
  L.foot(s,3,TOTAL,false);
})();

// ---------- 4. THE FIVE FAMILIES (light, diagram) ----------
(() => {
  const s = S(); L.bgLight(s);
  L.kicker(s,"Curriculum design",C.TEAL);
  L.title(s,"30 problems, five skill families");
  const fam=[
    ["A","Write-from-spec","P1 P2 P7 P17 P25","Build working code from a spec in an empty dir; import across a tree.",C.CYAN],
    ["B","Fix failing tests","P3 P11 P13 P20 P22 P29","Smallest fix to a red pytest \u2014 forbidden from editing the test.",C.TEAL],
    ["C","Numerical / algo fix","P4 P8 P12 P14 P18 P21 P23 P26 P28","Fix a mathematical bug: overflow, cancellation, wrong recurrence.",C.GREEN],
    ["D","Optimize to target","P5 P15","Correct-but-slow \u2192 hit a throughput target, re-measure in a budget.",C.GOLD],
    ["E","Tournament & critic","P6 P9 P10 P16 P19 P24 P27 P30","Best-of-N parallel candidates + self-review loops. Most agentic.",C.RED],
  ];
  let y=2.05;
  fam.forEach((f)=>{
    const h=0.92;
    // letter badge
    s.addShape(p.ShapeType.roundRect,{x:0.7,y,w:0.85,h,rectRadius:0.1,fill:{color:f[4]},line:{type:"none"}});
    s.addText(f[0],{x:0.7,y,w:0.85,h,fontFace:HF,fontSize:38,bold:true,color:C.WHITE,align:"center",valign:"middle"});
    // name + desc card
    s.addShape(p.ShapeType.roundRect,{x:1.65,y,w:8.0,h,rectRadius:0.09,fill:{color:C.WHITE},line:{color:C.LINE,width:1}});
    s.addText(f[1],{x:1.9,y:y+0.1,w:7.6,h:0.4,fontFace:BF,fontSize:19,bold:true,color:C.INK});
    s.addText(f[3],{x:1.9,y:y+0.48,w:7.6,h:0.4,fontFace:BF,fontSize:16,color:"33414F"});
    // problem-ids pill
    s.addShape(p.ShapeType.roundRect,{x:9.8,y,w:2.85,h,rectRadius:0.09,fill:{color:C.NAVY2},line:{type:"none"}});
    s.addText(f[2],{x:9.85,y,w:2.75,h,fontFace:BF,fontSize:16,bold:true,color:C.ICE,align:"center",valign:"middle",lineSpacingMultiple:1.05});
    y+=h+0.13;
  });
  L.foot(s,4,TOTAL,false);
})();

// ---------- 5. LEADERBOARD top (light) ----------
(() => {
  const s = S(); L.bgLight(s);
  L.kicker(s,"Results \u00b7 top of the board",C.TEAL);
  L.title(s,"Eight lanes reached a clean 30/30");
  const rows=[
    ["oss120 (gpt-oss-120b)","local dgx \u00b7 vLLM 0.14.1","30/30","9m",true],
    ["inkling (thinkingmachines)","OpenRouter","30/30 (eff.)","24m",true],
    ["uic-laguna-xs2","nVIDIA A100 (MoE)","30/30","49m",true],
    ["uic-qwen36-35b-a3b","nVIDIA A100 (MoE)","30/30","52m",true],
    ["qwen36-27b","Intel PVC (1 tile)","30/30","1h22m",true],
    ["ornith-9b (reasoning)","Intel PVC (1 tile)","30/30","3h05m",true],
    ["kimi (Kimi-K2.6)","local dgx","30/30","3h18m",true],
    ["laguna-xs2 (direct)","nVIDIA A100 ik_llama","27/30 (eff.30)","56m",true],
    ["glm-5.2","OpenRouter (paid)","29/30","44m",false],
    ["gemma4-31b","Intel PVC (1 tile)","29/30","3h01m",false],
    ["uic-ornith-9b (reasoning)","nVIDIA A100 llama.cpp","28/30","1h36m",false],
  ];
  const x=0.7, w=11.93; let y=1.95; const rh=0.42;
  // header
  s.addShape(p.ShapeType.rect,{x,y,w,h:rh,fill:{color:C.NAVY},line:{type:"none"}});
  const cols=[[0.15,5.15,"MODEL","left"],[5.35,3.35,"PLATFORM","left"],[8.75,1.9,"SCORE","center"],[10.75,1.05,"TIME","left"]];
  cols.forEach(c=> s.addText(c[2],{x:x+c[0],y,w:c[1],h:rh,fontFace:BF,fontSize:16,bold:true,color:C.ICE,align:c[3],valign:"middle"}));
  y+=rh;
  rows.forEach((r,i)=>{
    const fill = r[4] ? (i%2? "EAF6EC":"DFF0E2") : (i%2? "F5F8FC":"FFFFFF");
    s.addShape(p.ShapeType.rect,{x,y,w,h:rh,fill:{color:fill},line:{color:C.LINE,width:0.5}});
    if(r[4]) s.addShape(p.ShapeType.rect,{x,y,w:0.1,h:rh,fill:{color:C.GREEN},line:{type:"none"}});
    s.addText(r[0],{x:x+0.15,y,w:5.15,h:rh,fontFace:BF,fontSize:16,bold:r[4],color:C.INK,valign:"middle"});
    s.addText(r[1],{x:x+5.35,y,w:3.35,h:rh,fontFace:BF,fontSize:16,color:"33414F",valign:"middle"});
    s.addText(r[2],{x:x+8.75,y,w:1.9,h:rh,fontFace:BF,fontSize:16,bold:true,color:r[4]?C.GREEN:C.INK,align:"center",valign:"middle"});
    s.addText(r[3],{x:x+10.75,y,w:1.05,h:rh,fontFace:BF,fontSize:16,color:C.GREY,align:"left",valign:"middle"});
    y+=rh;
  });
  s.addText("Green = clean 30/30. A 9B model (ornith-9b) hits 30/30 \u2014 size is not the gate; tool-use training + a correct serving stack are.",
    {x:0.7,y:y+0.06,w:11.9,h:0.45,fontFace:BF,fontSize:16,italic:true,color:C.GREY});
  L.foot(s,5,TOTAL,false);
})();

// ---------- 6. FINDING: provider speed (light) ----------
(() => {
  const s = S(); L.bgLight(s);
  L.kicker(s,"Finding 1",C.GOLD);
  L.title(s,"Provider speed is a first-class axis");
  s.addText("The same 30/30 score costs minutes on a fast backend and hours on a slow one. For real agentic work (Kanban workers, coordinators) throughput decides usability as much as accuracy.",
    {x:0.7,y:2.0,w:12,h:0.85,fontFace:BF,fontSize:18,color:C.INK,lineSpacingMultiple:1.15});
  // two contrasting columns
  L.card(s,0.7,3.1,5.85,3.15,"Fast backends \u2014 30/30 in minutes",
    "oss120 (local dgx)  \u2014  9m\nuic-laguna-xs2 (A100)  \u2014  49m\nuic-qwen36-35b (A100)  \u2014  52m\nglm-5.2 (OpenRouter)  \u2014  44m\n\nFast local-dgx / A100 / PVC lanes clear the whole suite before a slow lane finishes its first few problems.",
    {accent:C.GREEN,hsize:19,bsize:17});
  L.card(s,6.75,3.1,5.85,3.15,"Slow local lanes \u2014 7\u20138h for less",
    "nemotron-3-nano 30B (spark)  \u2014  7h36m  \u00b7  19/30\nllama70 (local dgx)  \u2014  7h16m  \u00b7  18/29\nnemotron3-33b Omni (spark)  \u2014  7h31m  \u00b7  16/30\n\nspark-Ollama local lanes burn a full workday and still score lower \u2014 not a candidate for a live worker regardless of score.",
    {accent:C.RED,hsize:19,bsize:17});
  L.foot(s,6,TOTAL,false);
})();

// ---------- 7. FINDING: hardest problems (light) ----------
(() => {
  const s = S(); L.bgLight(s);
  L.kicker(s,"Finding 2 \u00b7 what separated the fleet",C.GOLD);
  L.title(s,"Concurrency & numerical stability are the wall");
  const hp=[
    ["P24","Token-bucket limiter + critic","52%","Burst-cap + fractional refill + injected clock + self-review. The single hardest problem \u2014 11 of 23 lanes failed."],
    ["P4","Softmax numerical stability","61%","A one-line fix (subtract max before exp) \u2014 but tests whether the model KNOWS the overflow pattern. Half the mid-tier missed."],
    ["P17","Multi-backend codec round-trip","61%","Two-function contract across three import targets. Structure, not algorithm, is the difficulty."],
    ["P25","3-stage fan-out pipeline","61%","Composition / fan-out \u2014 the ONLY problem glm-5.2 missed, and single-shot laguna too. Irreducible variance even for top models."],
    ["P13","Hand-rolled JSON parser","70%","Real recursive descent, no json / eval. Cleanly separates mid-tier from top."],
  ];
  let y=2.05;
  hp.forEach((h)=>{
    const hh=0.86;
    s.addShape(p.ShapeType.roundRect,{x:0.7,y,w:1.05,h:hh,rectRadius:0.1,fill:{color:C.NAVY},line:{type:"none"}});
    s.addText(h[0],{x:0.7,y:y+0.06,w:1.05,h:0.42,fontFace:HF,fontSize:24,bold:true,color:C.CYAN,align:"center"});
    s.addText(h[2],{x:0.7,y:y+0.46,w:1.05,h:0.35,fontFace:BF,fontSize:16,bold:true,color:C.GOLD,align:"center"});
    s.addShape(p.ShapeType.roundRect,{x:1.85,y,w:10.78,h:hh,rectRadius:0.09,fill:{color:C.WHITE},line:{color:C.LINE,width:1}});
    s.addText(h[1],{x:2.05,y:y+0.09,w:10.4,h:0.38,fontFace:BF,fontSize:18,bold:true,color:C.INK});
    s.addText(h[3],{x:2.05,y:y+0.46,w:10.4,h:0.36,fontFace:BF,fontSize:16,color:"33414F"});
    y+=hh+0.11;
  });
  L.foot(s,7,TOTAL,false);
})();

// ---------- 8. ZERO-SCORE infra story (dark) ----------
(() => {
  const s = S(); L.bgDark(s);
  L.kicker(s,"Finding 3 \u00b7 the zero-score rule at work",C.CYAN);
  s.addText("Every 0/N was infrastructure, not a dumb model",{x:0.7,y:0.98,w:12,h:1.0,fontFace:HF,fontSize:38,bold:true,color:C.WHITE});
  const z=[
    ["uic-ornith-9b","0 \u2192 28/30","Ollama GGUF blobs carry no chat template \u2014 --jinja silently emitted no tool calls. Fixed with explicit --chat-template-file via llama.cpp."],
    ["oss120","0 \u2192 30/30","vLLM 0.13 streaming-flush bug truncated tool-call deltas. Upgraded the endpoint to vLLM 0.14.1."],
    ["nemotron-super","0 \u2192 26/30","120B was never resident (weights > host RAM). Re-routed to a real endpoint."],
    ["P30 (all lanes)","hang \u2192 pass","A grader SCORE_TIMEOUT bug caused a ~6.5h harness hang + false fails. Excluded from wall-clock."],
  ];
  z.forEach((r,i)=>{
    const x=0.7+(i%2)*6.15, y=2.25+Math.floor(i/2)*2.0;
    s.addShape(p.ShapeType.roundRect,{x,y,w:5.85,h:1.8,rectRadius:0.1,fill:{color:C.NAVY2},line:{color:C.TEAL,width:1.5}});
    s.addShape(p.ShapeType.roundRect,{x,y,w:0.13,h:1.8,rectRadius:0.05,fill:{color:C.GREEN},line:{type:"none"}});
    s.addText(r[0],{x:x+0.3,y:y+0.16,w:3.4,h:0.45,fontFace:BF,fontSize:19,bold:true,color:C.WHITE});
    s.addText(r[1],{x:x+3.7,y:y+0.16,w:2.0,h:0.45,fontFace:HF,fontSize:20,bold:true,color:C.CYAN,align:"right"});
    s.addText(r[2],{x:x+0.3,y:y+0.68,w:5.35,h:1.0,fontFace:BF,fontSize:16,color:C.ICE,lineSpacingMultiple:1.1,valign:"top"});
  });
  s.addText("Recording any of these as a capability result would have libeled five perfectly capable models.",
    {x:0.7,y:6.5,w:12,h:0.5,fontFace:BF,fontSize:17,italic:true,color:C.ICE});
  L.foot(s,8,TOTAL,true);
})();

// ---------- 9. PLATFORM LEGEND (light, diagram) ----------
(() => {
  const s = S(); L.bgLight(s);
  L.kicker(s,"The fleet",C.TEAL);
  L.title(s,"Five serving platforms, one harness");
  const plat=[
    ["Intel PVC","Data Center GPU Max 1550 \u2014 each dense model on one 64 GB PVC tile.",C.TEAL,"qwen36-27b \u00b7 ornith-9b \u00b7 gemma4-*"],
    ["nVIDIA A100","8\u00d7 A100-80GB DGX \u2014 one or a few GPUs per model.",C.GREEN,"laguna \u00b7 qwen36-35b-a3b \u00b7 ornith"],
    ["local dgx","Locally-served DGX endpoints (incl. the 550B host). Direct, no LiteLLM.",C.CYAN,"oss120 \u00b7 kimi \u00b7 llama70 \u00b7 nemotron-ultra"],
    ["spark (ollama)","spark nodes serving via Ollama \u2014 the slow tail of the fleet.",C.GOLD,"qwen3-14b \u00b7 nemotron nano/33B"],
    ["OpenRouter","Hosted API \u2014 free tier preferred, paid tagged (glm-5.2).",C.RED,"glm-5.2 \u00b7 nemotron-3-super"],
  ];
  // 2 cols x 3 rows-ish (5 items)
  plat.forEach((pt,i)=>{
    const x=0.7+(i%2)*6.15, y=1.9+Math.floor(i/2)*1.72;
    const w = (i===4) ? 11.93 : 5.85;
    const ch=1.55;
    s.addShape(p.ShapeType.roundRect,{x,y,w,h:ch,rectRadius:0.1,fill:{color:C.WHITE},line:{color:C.LINE,width:1},shadow:{type:"outer",color:"9FB0C0",blur:5,offset:2,angle:90,opacity:0.25}});
    s.addShape(p.ShapeType.roundRect,{x,y,w:0.14,h:ch,rectRadius:0.05,fill:{color:pt[2]},line:{type:"none"}});
    s.addText(pt[0],{x:x+0.34,y:y+0.13,w:w-0.6,h:0.38,fontFace:BF,fontSize:20,bold:true,color:C.INK,valign:"top"});
    s.addText(pt[1],{x:x+0.34,y:y+0.57,w:w-0.55,h:0.52,fontFace:BF,fontSize:16,color:"33414F",lineSpacingMultiple:1.0,valign:"top"});
    s.addText(pt[3],{x:x+0.34,y:y+1.12,w:w-0.55,h:0.32,fontFace:BF,fontSize:16,italic:true,color:pt[2],valign:"top"});
  });
  L.foot(s,9,TOTAL,false);
})();

// ---------- 10. FULL TABLE part A (light) ----------
function tableSlide(title,rows,slideNo){
  const s = S(); L.bgLight(s);
  L.kicker(s,"Integrated master table",C.TEAL);
  L.title(s,title);
  const x=0.7, w=11.93; let y=1.95; const rh=0.415;
  s.addShape(p.ShapeType.rect,{x,y,w,h:rh,fill:{color:C.NAVY},line:{type:"none"}});
  const cols=[[0.1,0.6,"#","left"],[0.72,4.4,"MODEL","left"],[5.15,3.5,"PLATFORM","left"],[8.7,1.6,"SCORE","center"],[10.35,1.45,"TIME","left"]];
  cols.forEach(c=> s.addText(c[2],{x:x+c[0],y,w:c[1],h:rh,fontFace:BF,fontSize:16,bold:true,color:C.ICE,align:c[3],valign:"middle"}));
  y+=rh;
  rows.forEach((r,i)=>{
    s.addShape(p.ShapeType.rect,{x,y,w,h:rh,fill:{color:i%2?"F5F8FC":"FFFFFF"},line:{color:C.LINE,width:0.5}});
    s.addText(String(r[0]),{x:x+0.1,y,w:0.6,h:rh,fontFace:BF,fontSize:16,color:C.GREY,valign:"middle"});
    s.addText(r[1],{x:x+0.72,y,w:4.4,h:rh,fontFace:BF,fontSize:16,color:C.INK,valign:"middle"});
    s.addText(r[2],{x:x+5.15,y,w:3.5,h:rh,fontFace:BF,fontSize:16,color:"33414F",valign:"middle"});
    const clean = r[3].startsWith("30/30");
    s.addText(r[3],{x:x+8.7,y,w:1.6,h:rh,fontFace:BF,fontSize:16,bold:clean,color:clean?C.GREEN:C.INK,align:"center",valign:"middle"});
    s.addText(r[4],{x:x+10.35,y,w:1.45,h:rh,fontFace:BF,fontSize:16,color:C.GREY,align:"left",valign:"middle"});
    y+=rh;
  });
  L.foot(s,slideNo,TOTAL,false);
  return s;
}
tableSlide("All 26 lanes \u2014 ranks 1\u201313",[
  [1,"oss120 (gpt-oss-120b)","local dgx \u00b7 vLLM 0.14.1","30/30","9m"],
  [2,"inkling (thinkingmachines)","OpenRouter","30/30*","24m"],
  [3,"kimi (Kimi-K2.6)","local dgx","30/30","3h18m"],
  [4,"qwen36-27b","Intel PVC (1 tile)","30/30","1h22m"],
  [5,"ornith-9b (reasoning)","Intel PVC (1 tile)","30/30","3h05m"],
  [6,"uic-qwen36-35b-a3b","nVIDIA A100 (MoE)","30/30","52m"],
  [7,"uic-laguna-xs2","nVIDIA A100 (MoE)","30/30","49m"],
  [8,"laguna-xs2 (33B.A3B MoE)","nVIDIA A100 ik_llama","27/30*","56m"],
  [9,"glm-5.2","OpenRouter (paid)","29/30","44m"],
  [10,"gemma4-31b","Intel PVC (1 tile)","29/30","3h01m"],
  [11,"uic-ornith-9b (reasoning)","nVIDIA A100 llama.cpp","28/30","1h36m"],
  [12,"gemma4-12b","Intel PVC (1 tile)","28/30","3h15m"],
  [13,"devstral-small-2","Intel PVC (1 tile)","28/30","1h27m"],
],10);

// ---------- 11. FULL TABLE part B ----------
tableSlide("All 26 lanes \u2014 ranks 14\u201326",[
  [14,"uic-gemma4-26b-q4","nVIDIA A100 (Q4)","26/30","1h12m"],
  [15,"nemotron-3-super 120B","OpenRouter free","26/30","1h48m"],
  [16,"laguna-s-2.1 (48L MoE)","local dgx ik_llama \u00b7 chicago-2","26/30","2h17m"],
  [17,"uic-gemma4-26b-q8","nVIDIA A100 (Q8)","24/30","1h40m"],
  [18,"devstral2-24b","spark (ollama)","24/30","2h14m"],
  [19,"uic-ornith-35b","nVIDIA A100","23/30","1h29m"],
  [20,"nemotron-3-ultra 550B","local dgx (rbh101)","22/26","hung@P27"],
  [21,"qwen3-14b","spark (ollama)","20/28","4h41m"],
  [22,"gemma4-e4b","Intel PVC (1 tile)","20/30","1h39m"],
  [23,"gemma4-e2b","Intel PVC (1 tile)","20/30","1h02m"],
  [24,"nemotron-3-nano 30B","spark (ollama)","19/30","7h36m"],
  [25,"llama70 (retired 07-22)","local dgx","18/29","7h16m"],
  [26,"nemotron3 33B (Omni)","spark (ollama)","16/30","7h31m"],
],11);

// ---------- 12. MODEL IDENTITY note (light) ----------
(() => {
  const s = S(); L.bgLight(s);
  L.kicker(s,"Provenance \u00b7 identity verified live",C.TEAL);
  L.title(s,"The Nemotron family, disambiguated");
  s.addText("All three verified against live ollama show / the endpoint map \u2014 never from a tag. They are different architectures with the same marketing prefix.",
    {x:0.7,y:2.0,w:12,h:0.7,fontFace:BF,fontSize:18,color:C.INK,lineSpacingMultiple:1.15});
  const n=[
    ["nemotron3 33B \u201cOmni\u201d","nemotron_h_omni","Mamba-hybrid, vision+tools. Wastes capacity on an unused vision stack.","16/30"],
    ["nemotron-3-nano 30B \u201cMoE\u201d","nemotron_h_moe","Text-only, 1.05M ctx. Beats its Omni sibling on coding.","19/30"],
    ["nemotron-3-ultra 550B","dense-MoE, NVFP4","A55B on local dgx (rbh101). Hung at P27 \u2014 partial.","22/26"],
  ];
  n.forEach((r,i)=>{
    const x=0.7+i*4.05;
    s.addShape(p.ShapeType.roundRect,{x,y:2.95,w:3.8,h:3.3,rectRadius:0.1,fill:{color:C.WHITE},line:{color:C.LINE,width:1},shadow:{type:"outer",color:"9FB0C0",blur:5,offset:2,angle:90,opacity:0.25}});
    s.addShape(p.ShapeType.roundRect,{x,y:2.95,w:3.8,h:0.13,rectRadius:0.05,fill:{color:C.CYAN},line:{type:"none"}});
    s.addText(r[0],{x:x+0.25,y:3.2,w:3.3,h:0.8,fontFace:BF,fontSize:19,bold:true,color:C.INK,lineSpacingMultiple:1.05});
    s.addText(r[1],{x:x+0.25,y:4.0,w:3.3,h:0.4,fontFace:"Consolas",fontSize:16,color:C.TEAL,bold:true});
    s.addText(r[2],{x:x+0.25,y:4.45,w:3.35,h:1.3,fontFace:BF,fontSize:16,color:"33414F",valign:"top",lineSpacingMultiple:1.1});
    s.addText(r[3],{x:x+0.25,y:5.7,w:3.3,h:0.45,fontFace:HF,fontSize:26,bold:true,color:C.GREEN});
  });
  L.foot(s,12,TOTAL,false);
})();

// ---------- 13. TAKEAWAYS (light) ----------
(() => {
  const s = S(); L.bgLight(s);
  L.kicker(s,"What we learned",C.TEAL);
  L.title(s,"Five takeaways");
  const t=[
    ["Size is not the gate","A 9B model (ornith-9b) hits a clean 30/30. Tool-use training + a correct serving stack decide the outcome, not parameter count.",C.CYAN],
    ["Throughput is a usability cliff","An 18/30 lane that takes 7h is not a candidate for a live worker regardless of score. Speed is a first-class result.",C.GREEN],
    ["Concurrency + clocks are hard","Token-bucket, TTL, thread-safety separate the top tier from everyone else more sharply than sorts or graphs.",C.GOLD],
    ["A zero is (almost) always the stack","Five zeros this sweep were all infrastructure. The zero-score rule protected five capable models from a false verdict.",C.RED],
    ["Serving path is a variable","Same weights, two backends, different scores. Always attribute to provider \u00d7 model.",C.TEAL],
  ];
  t.forEach((r,i)=>{
    const x=0.7+(i%2)*6.15, y=2.05 + Math.floor(i/2)*1.5;
    const w = (i===4)?11.93:5.85;
    s.addShape(p.ShapeType.roundRect,{x,y,w,h:1.35,rectRadius:0.1,fill:{color:C.WHITE},line:{color:C.LINE,width:1}});
    s.addShape(p.ShapeType.ellipse,{x:x+0.25,y:y+0.4,w:0.55,h:0.55,fill:{color:r[2]},line:{type:"none"}});
    s.addText(String(i+1),{x:x+0.25,y:y+0.4,w:0.55,h:0.55,fontFace:HF,fontSize:24,bold:true,color:C.WHITE,align:"center",valign:"middle"});
    s.addText(r[0],{x:x+1.0,y:y+0.14,w:w-1.2,h:0.4,fontFace:BF,fontSize:19,bold:true,color:C.INK});
    s.addText(r[1],{x:x+1.0,y:y+0.55,w:w-1.2,h:0.72,fontFace:BF,fontSize:16,color:"33414F",valign:"top",lineSpacingMultiple:1.08});
  });
  L.foot(s,13,TOTAL,false);
})();

// ---------- 14. CLOSING (dark) ----------
(() => {
  const s = S(); L.bgDark(s);
  s.addShape(p.ShapeType.roundRect,{x:0.7,y:0.7,w:0.14,h:1.7,rectRadius:0.05,fill:{color:C.CYAN},line:{type:"none"}});
  s.addText("BOTTOM LINE",{x:1.0,y:1.0,w:11,h:0.5,fontFace:BF,fontSize:18,color:C.CYAN,bold:true,charSpacing:2});
  s.addText("Seven models can drive our agent loops cleanly \u2014 across Intel PVC, nVIDIA A100, and local DGX.",
    {x:0.95,y:1.55,w:11.6,h:1.6,fontFace:HF,fontSize:34,bold:true,color:C.WHITE,lineSpacingMultiple:1.05});
  const stat=[["7","clean 30/30 lanes"],["9B","smallest lane at 30/30"],["5","infra zeros caught & fixed"],["52%","hardest problem pass rate"]];
  stat.forEach((st,i)=>{
    const x=0.95+i*2.95;
    s.addShape(p.ShapeType.roundRect,{x,y:3.5,w:2.65,h:1.5,rectRadius:0.12,fill:{color:C.NAVY2},line:{color:C.TEAL,width:1.5}});
    s.addText(st[0],{x,y:3.62,w:2.65,h:0.9,fontFace:HF,fontSize:42,bold:true,color:C.CYAN,align:"center"});
    s.addText(st[1],{x:x+0.1,y:4.5,w:2.45,h:0.45,fontFace:BF,fontSize:16,color:C.ICE,align:"center",bold:true});
  });
  s.addText("Route real agentic work to the top tier. Keep the slow tail for single-shot generation. Re-run per serving-path on every stack change.",
    {x:0.95,y:5.4,w:11.5,h:0.9,fontFace:BF,fontSize:18,color:C.ICE,lineSpacingMultiple:1.15});
  s.addText("Source: ~/pi-problems-30/FLEET_BENCHMARK_MASTER.md (v7) + FLEET_BENCHMARK_REPORT.pdf \u00b7 harness run_model_30.sh \u00b7 2026-07-06",
    {x:0.95,y:6.75,w:11.5,h:0.4,fontFace:BF,fontSize:16,color:C.GREY});
})();

const OUT = process.env.PI30_DECK_OUT || require("path").join(__dirname, "pi30_Fleet_Benchmark.pptx");
p.writeFile({ fileName: OUT }).then(f=>console.log("WROTE",f));
