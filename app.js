const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const months = ["", "jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
let signosCache = [];

function periodo(signo) {
  return `${signo.dia_inicio} ${months[signo.mes_inicio]} — ${signo.dia_fim} ${months[signo.mes_fim]}`;
}

async function carregarSignos() {
  const grid = $("#zodiacGrid");
  try {
    const resposta = await fetch("/api/signos");
    if (!resposta.ok) throw new Error("Falha ao carregar signos");
    signosCache = await resposta.json();

    grid.innerHTML = signosCache.map(signo => `
      <article class="zodiac-card" style="--accent:${signo.cor}" tabindex="0" role="button" data-signo="${signo.id_signo}" aria-label="Ver detalhes de ${signo.nome_signo}">
        <div class="symbol">${signo.simbolo}</div>
        <h3>${signo.nome_signo}</h3>
        <p>${signo.resumo}</p>
        <div class="card-footer">
          <span>${signo.elemento}</span>
          <span>${periodo(signo)}</span>
        </div>
      </article>
    `).join("");

    $$(".zodiac-card").forEach(card => {
      card.addEventListener("click", () => abrirModal(Number(card.dataset.signo)));
      card.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") abrirModal(Number(card.dataset.signo));
      });
    });
  } catch (erro) {
    grid.innerHTML = `<p style="color:#ff8c9e">Não foi possível carregar os signos. Verifique se o servidor Flask está rodando.</p>`;
  }
}

function abrirModal(id) {
  const signo = signosCache.find(item => item.id_signo === id);
  if (!signo) return;
  $("#modalSymbol").textContent = signo.simbolo;
  $("#modalSymbol").style.color = signo.cor;
  $("#modalPeriod").textContent = periodo(signo);
  $("#modalTitle").textContent = signo.nome_signo;
  $("#modalSummary").textContent = signo.resumo;
  $("#modalElement").textContent = signo.elemento;
  $("#modalPlanet").textContent = signo.planeta_regente;
  $("#signModal").classList.add("open");
  $("#signModal").setAttribute("aria-hidden", "false");
  document.body.style.overflow = "hidden";
}

function fecharModal() {
  $("#signModal").classList.remove("open");
  $("#signModal").setAttribute("aria-hidden", "true");
  document.body.style.overflow = "";
}

$$('[data-close-modal]').forEach(el => el.addEventListener("click", fecharModal));
document.addEventListener("keydown", event => {
  if (event.key === "Escape") fecharModal();
});

$("#signForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector(".submit-button");
  const message = $("#formMessage");

  const payload = {
    nome: $("#nome").value.trim(),
    email: $("#email").value.trim(),
    data_nascimento: $("#data_nascimento").value
  };

  button.disabled = true;
  button.classList.add("loading");
  message.textContent = "";

  try {
    const resposta = await fetch("/api/descobrir", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const dados = await resposta.json();
    if (!resposta.ok) throw new Error(dados.erro || "Não foi possível calcular seu signo.");
    mostrarResultado(dados);
  } catch (erro) {
    message.textContent = erro.message;
  } finally {
    button.disabled = false;
    button.classList.remove("loading");
  }
});

function mostrarResultado(dados) {
  const card = $("#resultCard");
  const placeholder = card.querySelector(".result-placeholder");
  const content = card.querySelector(".result-content");

  $("#resultHello").textContent = `Olá, ${dados.usuario.nome.split(" ")[0]} ✦`;
  $("#resultSymbol").textContent = dados.simbolo;
  $("#resultSymbol").style.color = dados.cor;
  $("#resultPeriod").textContent = periodo(dados);
  $("#resultName").textContent = dados.nome_signo;
  $("#resultSummary").textContent = dados.resumo;
  $("#resultElement").textContent = dados.elemento;
  $("#resultPlanet").textContent = dados.planeta_regente;
  $("#traits").innerHTML = dados.caracteristicas.map(item => `
    <div class="trait"><b>${item.tipo}</b><span>${item.descricao}</span></div>
  `).join("");

  placeholder.style.display = "none";
  content.hidden = false;
  card.animate([
    { transform: "scale(.985)", opacity: .7 },
    { transform: "scale(1)", opacity: 1 }
  ], { duration: 420, easing: "cubic-bezier(.2,.8,.2,1)" });

  if (window.innerWidth < 980) {
    card.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

const dateInput = $("#data_nascimento");
const hoje = new Date();
dateInput.max = `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, "0")}-${String(hoje.getDate()).padStart(2, "0")}`;

carregarSignos();
