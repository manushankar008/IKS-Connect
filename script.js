// State data: [code, name, hue, tagline, "emoji label;..." items, polygon coordinates (lon lat pairs)]
const D=[
["JK","Jammu & Kashmir",200,"Paradise of the Himalaya","🧣 Pashmina;🌸 Saffron;🍵 Kahwa;🛶 Shikara;🍎 Apples;🏔️ Himalayas","74 37 75.5 37 77.8 35.5 78.5 34 79 33 78 32.5 76.8 33 76 32.6 75.3 32.8 74.5 34 73.5 35"],
["HP","Himachal Pradesh",160,"Land of the Deodars","🍎 Apples;🛕 Kullu temples;🧶 Kullu shawl;⛰️ Spiti;🥟 Siddu;🌲 Deodar","75.8 32.6 76.8 33 77.8 32.8 78.7 32 78.4 31 77.6 30.7 77 30.9 76.3 31.3 75.9 32"],
["PB","Punjab",45,"Land of five rivers","🌾 Wheat fields;🕌 Golden Temple;🥛 Lassi;💃 Bhangra;🫓 Makki di roti;🚜 Harvest","73.9 31.7 74.5 32.5 75.5 32.6 75.9 32 76.3 31.3 76.5 30.5 76 29.9 75 29.9 74.2 30.2 73.9 30.8"],
["UK","Uttarakhand",130,"Devbhoomi","🛕 Char Dham;🧘 Rishikesh yoga;🏔️ Nanda Devi;🍬 Bal mithai;🌊 Ganga;🐅 Corbett","77.6 30.7 78.4 31 79 31.4 80.2 30.6 80.2 29.9 79.5 28.9 78.7 29.3 78 30.1 77.6 30.2"],
["HR","Haryana",90,"Cradle of the Gita","🥛 Dairy;🤼 Wrestling;⚔️ Kurukshetra;🌾 Basmati;🎶 Ragini;🐂 Murrah buffalo","74.6 29.2 75 29.9 76 29.9 76.5 30.5 77 30.9 77.6 30.2 77.4 29 77.2 28.4 76.9 27.7 76.2 27.7 75.9 28.4 75.1 28.8"],
["RJ","Rajasthan",25,"Land of kings","🏰 Forts;🐪 Camel;🎨 Miniatures;🧵 Bandhani;🍛 Dal baati;💃 Ghoomar","69.5 24.2 70.3 24.4 71.2 24.3 72.1 24.5 72.8 23.9 73.4 23.5 74.5 23.9 74.6 24.4 75.8 24.7 76.6 24.6 77.3 25.2 77.9 25.6 78.2 26.5 77.6 27.2 76.9 27.7 76.2 27.7 75.9 28.4 75.1 28.8 74.6 29.2 73.9 29.7 72.8 29.2 71.7 28.2 70.8 28 70.2 27.7 70.3 26.2 69.6 25.4"],
["GJ","Gujarat",35,"Jewel of the west","🦁 Gir lions;🪔 Garba;🧵 Patola;🏜️ Rann of Kutch;🛕 Somnath;🍘 Dhokla","68.2 23.7 69.5 24.2 70.3 24.4 71.2 24.3 72.1 24.5 72.8 23.9 73.4 23.5 74.2 22.5 73.7 21.3 72.8 20.8 72.6 21.4 72.2 21.2 71.1 20.7 70.2 20.9 69 22.3 69.7 22.4 70.5 22.9 69.5 22.8 68.5 23.3"],
["UP","Uttar Pradesh",15,"Heartland of tradition","🕌 Taj Mahal;🪔 Varanasi ghats;🛕 Ayodhya;🍬 Petha;🎵 Kathak;🧶 Banarasi silk","77.5 29.8 78 30.1 78.7 29.3 79.5 28.9 80.2 28.7 81 28.4 81.9 27.8 83.3 27.4 84.6 27.2 84.6 26.4 83.9 25.6 83.5 24.5 82.5 24.4 81.6 25 80.3 26 79 26.3 78.2 26.4 77.6 27.2 77.2 28.4 77.5 29.2"],
["BR","Bihar",50,"Seat of Buddha's awakening","🛕 Mahabodhi;📚 Nalanda;🎨 Madhubani;🍘 Litti chokha;🌸 Chhath;🌰 Makhana","83.3 27.4 84.5 27.3 86 26.6 87.8 26.4 88.1 25.3 87.2 25.2 86.5 24.5 85.5 24.4 84.4 24.4 83.6 24.5 83.9 25.6 84.6 26.4"],
["JH","Jharkhand",120,"Land of forests","🌳 Sal forests;🥁 Sarhul;🌊 Hundru falls;🎨 Sohrai art;⛏️ Minerals;🐘 Betla","83.5 24.5 84.4 24.4 85.5 24.4 86.5 24.5 87.5 24.8 87.9 23.6 87.2 22.6 86.4 22.5 85.5 22.1 84.7 22.4 84 23 83.3 23.7"],
["WB","West Bengal",340,"Land of letters and art","🐅 Sundarbans;🍬 Rasgulla;🎭 Durga Puja;📖 Tagore;🍵 Darjeeling tea;🐟 Hilsa","88.1 26.5 88.6 26.3 89.8 26.7 89.1 25.3 88.7 24.5 88.6 23.3 89 22 88.3 21.6 87.2 21.6 86.8 22.2 86.4 22.5 87.2 22.6 87.9 23.6 87.5 24.8 88.1 25.3"],
["SK","Sikkim",280,"Abode of Kanchenjunga","🏔️ Kanchenjunga;🪷 Orchids;🧘 Monasteries;🥟 Momos;🍵 Cardamom;🎭 Cham dance","88 27.9 88.9 28 88.9 27.1 88.4 27"],
["AS","Assam",140,"Land of the red river","🍵 Assam tea;🦏 One-horned rhino;🧵 Muga silk;💃 Bihu;🌊 Brahmaputra;🍚 Pitika","89.8 26.7 91 27 92.5 27 94 27.6 95.8 27.5 95.2 26.4 94.5 25.9 93.6 25.4 92.8 25 92.2 24.9 91.5 24.2 90.7 25.2 89.9 25.3"],
["AR","Arunachal Pradesh",170,"Land of dawn-lit mountains","⛰️ Tawang;🧘 Monastery;🧶 Apatani weave;🦜 Hornbill;🌸 Orchids;🎭 Mask dance","91.6 27.8 93 28.3 94.8 29.2 96.2 29 97.2 28 96.3 27.2 95.8 27.5 94 27.6 92.5 27 91.5 27"],
["NL","Nagaland",10,"Land of festivals","🦜 Hornbill Festival;🧶 Naga shawl;🌶️ Bhut jolokia;🪘 War dance;🏞️ Dzukou;🍲 Axone","93.6 25.4 94.5 25.9 95.2 26.4 95.2 25.4 94.4 25.2"],
["MN","Manipur",320,"Jewel of the east","💃 Ras Lila;🏑 Polo;🌸 Siroy lily;🦌 Sangai;🧵 Moirang phee;🏞️ Loktak","93.4 24.8 94.4 25.2 95.2 25.4 94.7 24 94.2 23.4 93.4 24"],
["MZ","Mizoram",150,"Land of the hill people","💃 Cheraw;🎋 Bamboo;🧵 Puanchei;🏔️ Blue Mountain;🎶 Chapchar Kut;🌿 Anthurium","92.3 24.1 93.4 24 93 22.5 92.5 22.9 92.2 23.5"],
["TR","Tripura",100,"Land of fourteen gods","🛕 Ujjayanta;🎋 Bamboo craft;🧵 Risa;💃 Hojagiri;🍍 Queen pineapple;🗿 Unakoti","91.2 24.2 92.2 24.2 91.8 23.1 91.4 23"],
["ML","Meghalaya",175,"Abode of clouds","🌉 Root bridges;☁️ Cherrapunji;🌊 Nohkalikai;🥁 Wangala;🛶 Dawki;🍲 Jadoh","89.8 25.8 91.5 26 92.8 25.8 92.2 25 91.5 25.1 90.5 25.1 89.9 25.3"],
["OD","Odisha",20,"Land of temples","🛕 Konark Sun;🛕 Jagannath;💃 Odissi;🎨 Pattachitra;🐢 Olive ridley;🍬 Rasabali","82.3 21.5 83.6 22.1 84.7 22.4 85.5 22.1 86.4 22.5 87 21.6 86.8 20.9 86.2 20 85 19.4 84.2 18.9 83.4 18.6 82.4 18 81.8 18.8 82.3 20 82.1 21"],
["CG","Chhattisgarh",110,"Rice bowl of India","🌳 Bastar;⛏️ Dhokra;🥁 Panthi;🌊 Chitrakote;🌾 Rice bowl;🛕 Sirpur","80.3 21.7 81 22.4 82 23 82.8 23.9 83.6 24.5 84 23 84.7 22.4 83.6 22.1 82.3 21.5 82.1 21 82.3 20 81.8 18.8 81.3 17.9 80.8 18.2 80.4 19.5 80.6 20.5"],
["MP","Madhya Pradesh",30,"Heart of India","🛕 Khajuraho;🏯 Sanchi;🐅 Tiger reserves;🧵 Chanderi;🎶 Tansen;💎 Panna","74.2 22.5 74.5 23.9 74.6 24.4 75.8 24.7 76.6 24.6 77.3 25.2 77.9 25.6 78.2 26.4 79 26.3 80.3 26 81.6 25 82.5 24.4 82.8 23.9 82 23 81 22.4 80.3 21.7 79.5 21.6 78.5 21.7 77.5 21.6 76.5 21.5 75.5 21.7 74.7 21.9"],
["MH","Maharashtra",5,"Land of Sahyadri","🛕 Ajanta & Ellora;🎬 Mumbai;🥭 Alphonso;🎶 Lavani;🍛 Vada pav;🚩 Maratha forts","72.8 20.8 73.7 21.4 74.2 22.2 74.7 21.9 75.5 21.7 76.5 21.5 77.5 21.6 78.5 21.7 79.5 21.6 80.3 21.7 80.6 20.5 80.4 19.5 80 18.8 79.2 18.9 78.4 19.5 77.6 19.4 77 18.6 76.2 18 75.5 17.5 75 16.5 74.4 15.8 73.7 16.2 73.3 17.5 72.8 19"],
["GA","Goa",190,"Pearl of the Orient","🏖️ Beaches;⛪ Basilica;🍤 Seafood;🎭 Carnival;🥂 Feni;🏰 Forts","73.7 15.8 74.3 15.8 74.1 15 73.8 15.2"],
["KA","Karnataka",350,"One state, many worlds","🏛️ Hampi;👑 Mysore Dasara;☕ Coorg coffee;🎭 Yakshagana;🍚 Bisi bele bath;🧵 Mysore silk","74.4 15.8 75 16.5 75.5 17.5 76.2 17.6 77.2 17.3 77.2 16 77.6 15.4 78.1 14.4 77.8 13.5 78.2 12.8 77.5 12.1 77.1 11.7 76.5 11.9 75.8 12 75.4 13 74.9 13.9 74.4 14.9"],
["KL","Kerala",160,"God's own country","🛶 Backwaters;🎭 Kathakali;🌶️ Spices;🐘 Thrissur Pooram;🥥 Coconut;🥋 Kalaripayattu","75.1 12.5 75.8 12 76.5 11.9 77.1 11.5 77.3 10 77.1 8.6 76.5 8.4 76.3 9.5 75.8 11"],
["TN","Tamil Nadu",355,"Land of temples & Tamil","🛕 Meenakshi;🎶 Carnatic;💃 Bharatanatyam;🧵 Kanchipuram silk;🍛 Idli & dosa;🗿 Mahabalipuram","76.5 11.9 77.5 12.1 78.2 12.8 79.6 13.3 80.3 13.4 80 11.6 79.8 10.3 79.2 9.5 78.5 8.9 77.5 8.1 77.2 8.4 77.1 8.6 77.3 10 77.1 11.5"],
["TG","Telangana",270,"Land of Deccan heritage","🕌 Charminar;🍚 Hyderabadi biryani;💎 Pearls;🏰 Golconda;🧵 Pochampally;🌸 Bathukamma","77.6 19.4 78.4 19.5 79.2 18.9 80 18.8 80.4 18.5 81.2 17.9 80.8 17.2 80.3 16.6 79.2 16.5 78.4 16.2 77.7 16.6 77.2 17.3 77 18.6"],
["AP","Andhra Pradesh",210,"Rice bowl of the south","🛕 Tirupati;🌶️ Guntur chilli;🎶 Kuchipudi;🎨 Kalamkari;🏞️ Araku;🍚 Pulihora","77.2 16 77.7 16.6 78.4 16.2 79.2 16.5 80.3 16.6 80.8 17.2 81.3 17.9 82.4 18 83.4 18.6 84.2 18.9 84.8 19 84.5 18.2 83.5 17.4 82.3 16.5 81.3 16.2 80.3 15.5 80.1 14.5 80.3 13.4 79.6 13.3 78.2 12.8 78.1 14.4 77.6 15.4"]
];

// DOM helpers
const $=id=>document.getElementById(id),NS="http://www.w3.org/2000/svg";
const map=$("map"),info=$("info"),chat=$("chat"),home=$("home"),msgs=$("msgs"),q=$("q");
const items=s=>s[4].split(";").map(t=>{const i=t.indexOf(" ");return{e:t.slice(0,i),l:t.slice(i+1)}});
let cur=null;

// Draw the map
D.forEach(s=>{
  const n=s[5].split(" ").map(Number),pts=[];
  for(let i=0;i<n.length;i+=2)pts.push(((n[i]-67.5)*15).toFixed(1)+","+((37.5-n[i+1])*15).toFixed(1));
  const p=document.createElementNS(NS,"polygon");
  p.setAttribute("points",pts.join(" "));p.setAttribute("class","st");p.setAttribute("tabindex","0");
  p.setAttribute("role","button");p.setAttribute("aria-label",s[1]);
  p.style.fill=`hsl(${s[2]} 58% 48%)`;
  const show=()=>{info.innerHTML=`<div class="kicker">${s[0]}</div><h2 class="disp">${s[1]}</h2><p>${s[3]}</p><div class="chips">${items(s).map(i=>`<span class="chip">${i.e} ${i.l}</span>`).join("")}</div><p style="margin-top:12px;color:var(--gold)">Click to open the guide →</p>`};
  p.onmouseenter=p.onfocus=show;p.onclick=()=>openState(s);
  p.onkeydown=e=>{if(e.key==="Enter")openState(s)};
  map.appendChild(p);
});

// Collage tile positions: [left %, top %, rotation, size px]
const slots=[[3,6,-6,170],[22,2,4,150],[44,8,-3,180],[68,3,6,160],[84,12,-5,150],[2,38,5,150],[88,42,-4,170],[5,70,-5,180],[24,78,4,150],[48,80,-3,170],[70,75,6,150],[86,72,-6,140]];

function openState(s){
  cur=s;chat.style.setProperty("--h",s[2]);
  $("cn").textContent=s[1];$("ct").textContent=s[3];$("wm").textContent=s[1];
  const it=items(s);
  $("collage").innerHTML=slots.map((sl,i)=>{const x=it[i%it.length];
    return `<div class="tile" style="left:${sl[0]}%;top:${sl[1]}%;width:${sl[3]}px;height:${sl[3]*.85}px;rotate:${sl[2]}deg;animation-delay:${-i*.8}s;background:linear-gradient(135deg,hsl(${s[2]+i*14} 70% 52%),hsl(${s[2]+i*14+35} 60% 28%))"><b>${x.e}</b><span>${x.l}</span></div>`}).join("");
  $("sg").innerHTML=it.slice(0,5).map(x=>`<button>${x.e} Tell me about ${x.l}</button>`).join("");
  [...$("sg").children].forEach((b,i)=>b.onclick=()=>ask(`Tell me about ${it[i].l}`));
  msgs.innerHTML="";
  add("a",`Namaste! I'm the <b>${s[1]}</b> guide. Ask me about its scriptures, arts, temples, food or festivals — I'll answer from the knowledge graph and show where each fact comes from.`);
  home.classList.remove("on");chat.classList.add("on");q.focus();
}

function add(r,h,src){
  const d=document.createElement("div");
  d.className="m "+r;
  d.innerHTML=h+(src?`<div class="src">${src.map(x=>`<i>${x}</i>`).join("")}</div>`:"");
  msgs.appendChild(d);msgs.scrollTop=msgs.scrollHeight;return d;
}

// Replace this with the real RAG call: fetch('/api/ask',{method:'POST',body:JSON.stringify({state:s[0],question})})
async function askBackend(s,text){
  await new Promise(r=>setTimeout(r,900));
  const it=items(s),low=text.toLowerCase();
  const hit=it.find(x=>low.includes(x.l.toLowerCase().split(" ")[0]))||it[Math.floor(Math.random()*it.length)];
  return{html:`${hit.e} <b>${hit.l}</b> is one of the nodes linked to ${s[1]} in the graph. This is a placeholder answer — once the RAG layer is connected, a grounded explanation drawn from the source texts will appear here.`,
    src:[`KG: ${s[1]} → ${hit.l}`,"Source: (to be linked)"]};
}

async function ask(text){
  text=text.trim();if(!text)return;q.value="";add("u",text.replace(/</g,"&lt;"));
  const t=add("a",'<span class="typing"><span></span><span></span><span></span></span>');
  const r=await askBackend(cur,text);t.remove();add("a",r.html,r.src);
}

// Events
$("send").onclick=()=>ask(q.value);
q.onkeydown=e=>{if(e.key==="Enter")ask(q.value)};
$("back").onclick=()=>{chat.classList.remove("on");home.classList.add("on")};
$("tb").onclick=()=>{
  const r=document.documentElement,l=r.dataset.theme?r.dataset.theme==="light":!matchMedia("(prefers-color-scheme: dark)").matches;
  r.dataset.theme=l?"dark":"light";
};
