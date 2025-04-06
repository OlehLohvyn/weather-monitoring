export function renderPagination(previous, next, onPageChange) {
    const container = document.getElementById("pagination");
    container.innerHTML = "";
  
    if (previous) {
      const btn = document.createElement("button");
      btn.innerText = "← Назад";
      btn.onclick = () => onPageChange(previous);
      container.appendChild(btn);
    }
  
    if (next) {
      const btn = document.createElement("button");
      btn.innerText = "Вперед →";
      btn.onclick = () => onPageChange(next);
      container.appendChild(btn);
    }
  }
  