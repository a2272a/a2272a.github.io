/* =========================================================
   갤럭시 S26 사전예약 팝업 로직
   ========================================================= */
(function s26PopupInit(){
  const popup = document.getElementById("s26Popup");
  const btnClose = document.getElementById("s26PopClose");
  const chk = document.getElementById("s26Hide24");
  if(!popup || !btnClose || !chk) return;

  const KEY = "S26_POPUP_HIDE_UNTIL";
  const readUntil = () => Number(localStorage.getItem(KEY) || "0");

  const open = () => {
    popup.classList.add("show");
    popup.setAttribute("aria-hidden","false");
    document.body.style.overflow = "hidden";
  };
  const close = () => {
    popup.classList.remove("show");
    popup.setAttribute("aria-hidden","true");
    document.body.style.overflow = "";
  };

  // 숨김 기간 체크
  const until = readUntil();
  if(Date.now() >= until){
    // 인터넷 팝업이 표시되지 않을 때만 S26 팝업 표시
    setTimeout(() => {
      const inetPopup = document.getElementById("inetPopup");
      if(!inetPopup || !inetPopup.classList.contains("show")) {
        open();
      }
    }, 500);
  }

  // X 닫기
  btnClose.addEventListener("click", ()=>{
    if(chk.checked){
      localStorage.setItem(KEY, String(Date.now() + 24*60*60*1000));
    }else{
      localStorage.removeItem(KEY);
    }
    close();
  });

  // 바깥 클릭 닫기
  popup.addEventListener("click", (e)=>{
    if(e.target === popup){
      if(chk.checked){
        localStorage.setItem(KEY, String(Date.now() + 24*60*60*1000));
      }else{
        localStorage.removeItem(KEY);
      }
      close();
    }
  });

  // ESC 닫기
  window.addEventListener("keydown", (e)=>{
    if(e.key === "Escape" && popup.classList.contains("show")){
      if(chk.checked){
        localStorage.setItem(KEY, String(Date.now() + 24*60*60*1000));
      }else{
        localStorage.removeItem(KEY);
      }
      close();
    }
  });
})();
