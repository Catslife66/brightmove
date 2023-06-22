// Load map
window.addEventListener("DOMContentLoaded", showMap)

async function showMap(){
    let objId = document.getElementById('object').dataset.id;
    let data = await fetchLocationData(objId);
    (g=>{var h,a,k,p="The Google Maps JavaScript API",
        c="google",
        l="importLibrary",
        q="__ib__",
        m=document,
        b=window;
        b=b[c]||(b[c]={});
        var d=b.maps||(b.maps={}),
        r=new Set,
        e=new URLSearchParams,
        u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));
        e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);
        e.set("callback",c+".maps."+q);
        a.src=`https://maps.${c}apis.com/maps/api/js?`+e;
        d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));
        a.nonce=m.querySelector("script[nonce]")?.nonce||"";
        m.head.append(a)}));
        d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})({
            key: data.api_key,
            v: "weekly",
    });
    let map;
    initMap(data);
}

async function fetchLocationData(objId) {
    let url = `/property/${objId}/map/`
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(error);
        throw error;
    }
}

async function initMap(data) {
  const position = data.location_coor;
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  map = new Map(document.getElementById("map"), {
    zoom: 14,
    center: position,
    mapId: `map-${data.property_id}`,
  });

  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    title: JSON.stringify(position),
  });
}


// like button functions
const btn = document.getElementById('like-btn')

btn.addEventListener('click', ()=>{
    let id = btn.dataset.id
    handleLikeBtn(id)
})

function handleLikeBtn(id){
    const xhr = new XMLHttpRequest()
    xhr.open('POST', `/property/${id}/add-to-wishlist/`, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const likeIcon = document.getElementById('like-icon')
            if(response.liked){
                likeIcon.setAttribute ('fill', "currentColor")
            }else {
                likeIcon.setAttribute ('fill', "none")
            }
        }
    }
    xhr.send();
}