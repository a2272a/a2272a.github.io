// 인터넷TV 팝업 로직 수정 - S26 팝업 우선 순위 적용
(function() {
  // S26 팝업 닫힘 이벤트 감지
  const s26Popup = document.getElementById("s26Popup");
  const inetPopup = document.getElementById("inetPopup");
  
  if(!s26Popup || !inetPopup) return;
  
  // S26 팝업이 닫힐 때 인터넷TV 팝업 확인
  const observer = new MutationObserver(() => {
    if(!s26Popup.classList.contains("show")) {
      // S26이 닫혔고, 인터넷TV 팝업 조건 확인
      const KEY = "INET_POPUP_HIDE_UNTIL";
      const until = Number(localStorage.getItem(KEY) || "0");
      
      if(Date.now() >= until && !inetPopup.classList.contains("show")) {
        setTimeout(() => {
          inetPopup.classList.add("show");
          inetPopup.setAttribute("aria-hidden","false");
          document.body.style.overflow = "hidden";
        }, 300);
      }
    }
  });
  
  observer.observe(s26Popup, { attributes: true, attributeFilter: ['class'] });
})();
