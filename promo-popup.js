/* =========================================================
   통합 프로모션 팝업 로직 (S26 + 인터넷TV)
   ========================================================= */
(function promoPopupInit(){
  // DOM이 완전히 로드된 후 실행
  if(document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
  function init() {
    const popup = document.getElementById("promoPopup");
    const btnClose = document.getElementById("promoPopClose");
    const chk = document.getElementById("promoHide24");
    const tabs = document.querySelectorAll(".promoTab");
    const tabContents = document.querySelectorAll(".promoTabContent");
    
    // 디버깅: 요소 확인
    console.log("Promo popup init:", {
      popup: !!popup,
      btnClose: !!btnClose,
      chk: !!chk,
      tabs: tabs.length,
      tabContents: tabContents.length
    });
    
    if(!popup || !btnClose || !chk) {
      console.error("통합 팝업 요소를 찾을 수 없습니다.");
      return;
    }

    const KEY = "PROMO_POPUP_HIDE_UNTIL";
    const readUntil = () => Number(localStorage.getItem(KEY) || "0");

    const open = () => {
      popup.classList.add("show");
      popup.setAttribute("aria-hidden","false");
      document.body.style.overflow = "hidden";
      console.log("통합 팝업 열림");
    };
    
    const close = () => {
      popup.classList.remove("show");
      popup.setAttribute("aria-hidden","true");
      document.body.style.overflow = "";
      console.log("통합 팝업 닫힘");
    };

    // 탭 전환
    tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        const targetTab = tab.dataset.tab;
        
        // 모든 탭 비활성화
        tabs.forEach(t => t.classList.remove("active"));
        tabContents.forEach(tc => tc.classList.remove("active"));
        
        // 선택된 탭 활성화
        tab.classList.add("active");
        const targetContent = document.getElementById(targetTab + "Tab");
        if(targetContent) {
          targetContent.classList.add("active");
        }
      });
    });

    // 숨김 기간 체크
    const until = readUntil();
    console.log("팝업 숨김 체크:", { until, now: Date.now(), shouldShow: Date.now() >= until });
    
    if(Date.now() >= until){
      // 약간의 딜레이 후 표시 (DOM 안정화)
      setTimeout(() => {
        open();
      }, 100);
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
  }
})();
