    function createLegendaBox(key,value){
      const box=document.createElement('div');box.className='legenda-box';
      const title=document.createElement('h2');title.textContent='Legenda sugerida';
      const ta=document.createElement('textarea');ta.className='legenda-textarea';ta.id='leg_'+key;ta.value=value;
      const btn=document.createElement('button');btn.className='btn-copy-legenda';btn.id='btn_leg_'+key;btn.textContent='Copiar legenda';btn.onclick=()=>copySlideLeg(key);
      box.append(title,ta,btn);return box;
    }
    function setStatus(msg){document.getElementById('status').textContent=msg}
    function buildPreviews(){
      const grid=document.getElementById('slidesGrid');const cap=document.getElementById('singleCaption');
      grid.replaceChildren();cap.replaceChildren();
      if(!['unica','por_slide'].includes(LEGENDA_MODE)){setStatus('Modo de legenda inválido.');return}
      if(LEGENDA_MODE==='por_slide'&&LEGENDAS.length!==SLIDES_HTML.length){setStatus('Falta legenda para um slide.');return}
      SLIDES_HTML.forEach((_,i)=>{
        const wrap=document.createElement('section');wrap.className='slide-wrapper';
        const label=document.createElement('div');label.className='slide-label';label.innerHTML='<span>Slide '+(i+1)+'</span><span>'+LABELS[i]+'</span>';
        const scaler=document.createElement('div');scaler.className='slide-scaler';
        const slide=createSlideElement(i);scaler.appendChild(slide);
        const foot=document.createElement('div');foot.className='slide-footer';
        const btn=document.createElement('button');btn.className='btn alt';btn.textContent='Baixar PNG';btn.onclick=()=>downloadSinglePNG(i,btn);foot.appendChild(btn);
        wrap.append(label,scaler,foot);
        if(LEGENDA_MODE==='por_slide')wrap.appendChild(createLegendaBox('slide_'+i,LEGENDAS[i]));
        grid.appendChild(wrap);
        requestAnimationFrame(()=>slide.style.transform='scale('+(scaler.clientWidth/1080)+')');
      });
      if(LEGENDA_MODE==='unica')cap.appendChild(createLegendaBox('unica',LEGENDA_UNICA));
    }
    function copySlideLeg(key){
      const value=document.getElementById('leg_'+key).value;
      navigator.clipboard.writeText(value).then(()=>{const btn=document.getElementById('btn_leg_'+key);btn.textContent='Copiada!';setTimeout(()=>btn.textContent='Copiar legenda',2000)}).catch(()=>setStatus('Selecione e copie o texto da legenda.'));
    }
    async function renderSlide(index){
      await document.fonts.ready;
      const stage=document.getElementById('renderArea');
      const slide=createSlideElement(index);
      slide.classList.add('exporting');slide.style.transform='none';slide.style.position='relative';
      stage.replaceChildren(slide);
      await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
      try{return await html2canvas(slide,{width:1080,height:1350,scale:1,useCORS:true,backgroundColor:null,logging:false,scrollX:0,scrollY:0})}
      finally{stage.replaceChildren()}
    }
    async function downloadSinglePNG(index,button){
      button.disabled=true;setStatus('Gerando slide '+(index+1)+'...');
      try{const canvas=await renderSlide(index);const link=document.createElement('a');link.href=canvas.toDataURL('image/png');link.download='sextou_slide_'+String(index+1).padStart(2,'0')+'.png';link.click();setStatus('PNG baixado.')}
      catch(e){setStatus('Erro ao exportar: '+e.message)}finally{button.disabled=false}
    }
    async function downloadZIP(){
      const buttons=document.querySelectorAll('.btn');buttons.forEach(b=>b.disabled=true);
      try{const zip=new JSZip();for(let i=0;i<SLIDES_HTML.length;i++){setStatus('Gerando PNG '+(i+1)+' de '+SLIDES_HTML.length+'...');const canvas=await renderSlide(i);zip.file('sextou_slide_'+String(i+1).padStart(2,'0')+'.png',canvas.toDataURL('image/png').split(',')[1],{base64:true})}
        const blob=await zip.generateAsync({type:'blob'});const link=document.createElement('a');link.href=URL.createObjectURL(blob);link.download='sextou.zip';link.click();setTimeout(()=>URL.revokeObjectURL(link.href),5000);setStatus('ZIP baixado.')}
      catch(e){setStatus('Erro ao exportar: '+e.message)}finally{buttons.forEach(b=>b.disabled=false)}
    }
    async function downloadPDF(){
      const buttons=document.querySelectorAll('.btn');buttons.forEach(b=>b.disabled=true);
      try{const pdf=new window.jspdf.jsPDF({orientation:'portrait',unit:'px',format:[1080,1350]});for(let i=0;i<SLIDES_HTML.length;i++){setStatus('Montando PDF, slide '+(i+1)+' de '+SLIDES_HTML.length+'...');const canvas=await renderSlide(i);if(i)pdf.addPage([1080,1350],'portrait');pdf.addImage(canvas.toDataURL('image/jpeg',.95),'JPEG',0,0,1080,1350)}
        pdf.save('sextou.pdf');setStatus('PDF baixado.')}
      catch(e){setStatus('Erro ao exportar: '+e.message)}finally{buttons.forEach(b=>b.disabled=false)}
    }
    document.fonts.ready.then(buildPreviews);
    window.addEventListener('resize',()=>document.querySelectorAll('.slide-scaler').forEach(s=>{const slide=s.querySelector('.slide');if(slide)slide.style.transform='scale('+(s.clientWidth/1080)+')'}));
