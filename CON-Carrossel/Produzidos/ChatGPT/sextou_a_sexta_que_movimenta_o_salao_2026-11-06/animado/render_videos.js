const {chromium}=require('C:\\Users\\Jcluz\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules\\playwright');
const {spawn}=require('child_process');
const {once}=require('events');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
const root=path.dirname(__dirname);
const ffmpeg='C:\\Users\\Jcluz\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python313\\site-packages\\imageio_ffmpeg\\binaries\\ffmpeg-win-x86_64-v7.1.exe';
const durations=[8,17,21,22,27,23,12];
const fps=30, motionDuration=4, frameCount=fps*motionDuration;

async function render(index,browser){
  const id=String(index+1).padStart(2,'0');
  const page=await browser.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.join(root,'carrossel_sextou.html')).href,{waitUntil:'load'});
  await page.waitForFunction(()=>typeof createSlideElement==='function');
  await page.addStyleTag({content:'body{padding:0!important;overflow:hidden!important}body>header,body>main,body>section,body>.status{display:none!important}*{caret-color:transparent!important}'});
  await page.addScriptTag({path:path.join(__dirname,'motion.js')});
  const meta=await page.evaluate(i=>mountMotion(i),index);
  const out=path.join(__dirname,'videos',`sextou_slide_${id}.mp4`);
  const encoder=spawn(ffmpeg,['-y','-hide_banner','-loglevel','error','-f','image2pipe','-vcodec','mjpeg','-framerate',String(fps),'-i','pipe:0','-vf',`tpad=stop_mode=clone:stop_duration=${durations[index]-motionDuration},scale=out_color_matrix=bt709:out_range=tv,setsar=1,format=yuv420p`,'-c:v','libx264','-preset','medium','-crf','18','-profile:v','high','-level:v','4.1','-threads','2','-r',String(fps),'-t',String(durations[index]),'-an','-movflags','+faststart','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',out],{windowsHide:true,stdio:['pipe','ignore','pipe']});
  let log='';encoder.stderr.on('data',d=>log+=d.toString());
  const done=once(encoder,'close');
  for(let f=0;f<frameCount;f++){
    await page.evaluate(t=>seekMotion(t),f/fps);
    if([0,30,66,119].includes(f))await page.screenshot({path:path.join(__dirname,'qa',`slide_${id}_frame_${String(f).padStart(3,'0')}.png`)});
    const bytes=await page.screenshot({type:'jpeg',quality:96});
    if(!encoder.stdin.write(bytes))await once(encoder.stdin,'drain');
    if(f%30===0)console.log(`Slide ${id}: quadro ${f}/${frameCount}`);
  }
  encoder.stdin.end();
  const [code]=await done;
  await page.close();
  if(code!==0||errors.length)throw Error(`Slide ${id}: ${log} ${errors.join('; ')}`);
  console.log(`Slide ${id} pronto: ${durations[index]}s, ${meta.elements} elementos animados.`);
  return {slide:index+1,duration:durations[index],fps,width:1080,height:1350,animatedElements:meta.elements,text:meta.text,file:path.basename(out),browserErrors:errors};
}
(async()=>{
  const requested=process.argv.slice(2).map(n=>Number(n)-1);
  const indexes=requested.length?requested:[0,1,2,3,4,5,6];
  const browser=await chromium.launch({headless:true,executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'});
  const results=[];
  try{
    for(let i=0;i<indexes.length;i+=2)results.push(...await Promise.all(indexes.slice(i,i+2).map(n=>render(n,browser))));
    fs.writeFileSync(path.join(__dirname,requested.length?'render-partial.json':'render-manifest.json'),JSON.stringify(results,null,2));
  }finally{await browser.close()}
})().catch(e=>{console.error(e);process.exit(1)});
