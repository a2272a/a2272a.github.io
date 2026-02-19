/* =========================================================
   통합 프로모션 팝업 로직 (S26 + 인터넷TV)
   ========================================================= */
(function promoPopupInit(){
  if(document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
  function init() {
    const popup = document.getElementById("promoPopup");
    const card  = popup ? popup.querySelector(".promoPopCard") : null;
    const btnClose = document.getElementById("promoPopClose");
    const chk = document.getElementById("promoHide24");
    const tabs = document.querySelectorAll(".promoTab");
    const tabContents = document.querySelectorAll(".promoTabContent");
    
    if(!popup || !btnClose || !chk) return;

    const KEY = "PROMO_POPUP_HIDE_UNTIL";
    const readUntil = () => Number(localStorage.getItem(KEY) || "0");
    const isMobile = () => window.innerWidth <= 520 || /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent);

    const open = () => {
      // ✅ CSS 클래스 의존 없이 style 직접 제어
      popup.style.cssText = [
        "display:flex",
        "position:fixed",
        "top:0", "left:0", "right:0", "bottom:0",
        "width:100%", "height:100%",
        "background:rgba(0,0,0,0.75)",
        "z-index:999999",
        isMobile() ? "align-items:flex-end" : "align-items:center",
        "justify-content:center",
        isMobile() ? "padding:0" : "padding:20px",
        "box-sizing:border-box",
        "transform:none"
      ].join(";");

      if(card) {
        card.style.cssText = isMobile() ? [
          "position:relative",
          "width:100%", "max-width:100%",
          "max-height:90vh",
          "background:#fff",
          "border-radius:20px 20px 0 0",
          "overflow-y:auto",
          "-webkit-overflow-scrolling:touch",
          "box-shadow:0 20px 60px rgba(0,0,0,0.6)",
          "flex-shrink:0",
          "margin:0",
          "transform:none"
        ].join(";") : [
          "position:relative",
          "width:100%", "max-width:480px",
          "max-height:85vh",
          "background:#fff",
          "border-radius:20px",
          "overflow-y:auto",
          "-webkit-overflow-scrolling:touch",
          "box-shadow:0 20px 60px rgba(0,0,0,0.6)",
          "flex-shrink:0",
          "margin:auto",
          "transform:none"
        ].join(";");
      }

      popup.setAttribute("aria-hidden", "false");

      // iOS 스크롤 고정
      const scrollY = window.scrollY;
      popup._savedScrollY = scrollY;
      document.body.style.overflow = "hidden";
      if(isMobile()) {
        document.body.style.position = "fixed";
        document.body.style.width = "100%";
        document.body.style.top = `-${scrollY}px`;
      }
    };
    
    const close = () => {
      popup.style.display = "none";
      popup.setAttribute("aria-hidden", "true");

      // 스크롤 복원
      document.body.style.overflow = "";
      document.body.style.position = "";
      document.body.style.width = "";
      document.body.style.top = "";
      if(popup._savedScrollY !== undefined) {
        window.scrollTo(0, popup._savedScrollY);
      }
    };

    // 탭 전환
    tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        const targetTab = tab.dataset.tab;
        tabs.forEach(t => t.classList.remove("active"));
        tabContents.forEach(tc => tc.classList.remove("active"));
        tab.classList.add("active");
        const targetContent = document.getElementById(targetTab + "Tab");
        if(targetContent) {
          targetContent.classList.add("active");
          if(card) card.scrollTop = 0;
        }
      });
    });

    // 숨김 기간 체크 후 표시
    const until = readUntil();
    if(Date.now() >= until) {
      setTimeout(open, 300);
    }

    const saveAndClose = () => {
      if(chk.checked) localStorage.setItem(KEY, String(Date.now() + 24*60*60*1000));
      else localStorage.removeItem(KEY);
      close();
    };

    btnClose.addEventListener("click", saveAndClose);

    popup.addEventListener("click", (e) => {
      if(e.target === popup) saveAndClose();
    });

    window.addEventListener("keydown", (e) => {
      if(e.key === "Escape" && popup.style.display !== "none") saveAndClose();
    });

    if(card) {
      card.addEventListener("touchmove", e => e.stopPropagation(), { passive: true });
    }
  }
})();
