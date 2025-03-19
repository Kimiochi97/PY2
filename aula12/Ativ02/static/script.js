    var tarefas = [];

document.addEventListener("DOMContentLoaded", () => {
    carregarTarefas();
    setInterval(atualizarTempo, 200);
});

function carregarTarefas() {
    fetch("/tarefas")
        .then(response => response.json())
        .then(data => {
            tarefas = data;
            renderizarTarefas();
        })
        .catch(error => console.error("Erro ao carregar tarefas:", error));
}

function adicionarTarefa() {
    const nomeInput = document.getElementById("nomeTarefa");
    const duracaoInput = document.getElementById("duracaoTarefa");
    
    if (!nomeInput.value || !duracaoInput.value) {
        alert("Preencha os campos obrigatórios!");
        return;
    }

    const novaTarefa = {
        nome: nomeInput.value,
        descricao: document.getElementById("descricaoTarefa").value,
        duracao: parseInt(duracaoInput.value)
    };

    fetch("/tarefas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(novaTarefa)
    })
    .then(response => response.json())
    .then(data => {
        tarefas.push(data);
        renderizarTarefas(true);
    });

    nomeInput.value = "";
    document.getElementById("descricaoTarefa").value = "";
    duracaoInput.value = "";
}

function atualizarTempo() {
    const agora = Date.now();
    tarefas.forEach(tarefa => {
        const tempoRestante = tarefa.dataLimite - agora;
        tarefa.progresso = ((agora - tarefa.dataCriacao) / (tarefa.dataLimite - tarefa.dataCriacao)) * 100;
        if (tempoRestante <= 0 && !tarefa.expirada) {
            tarefa.expirada = true;
            exibirAlerta(`⏰ Tempo esgotado: ${tarefa.nome}`);
        }
    });
    renderizarTarefas();
}

function renderizarTarefas(novaAdicao = false) {
    const container = document.getElementById("listaTarefas");
    container.innerHTML = "";
    tarefas.forEach(tarefa => {
        const elemento = document.createElement("div");
        elemento.id = `tarefa-${tarefa.id}`;
        elemento.className = `cartao-tarefa${novaAdicao ? " nova" : ""}`;
        elemento.innerHTML = `
            <h3>${tarefa.nome}</h3>
            ${tarefa.descricao ? `<p>${tarefa.descricao}</p>` : ""}
            <div class="barra-progresso">
                <div class="progresso" style="width: ${Math.min(tarefa.progresso, 100)}%"></div>
            </div>
            <div class="contador-tempo">${formatarTempo(tarefa.dataLimite - Date.now())}</div>
            <button onclick="removerTarefa(${tarefa.id})">🗑️ Remover</button>
        `;
        if (tarefa.expirada) {
            elemento.classList.add("expirada");
        }
        container.appendChild(elemento);
    });
}

function formatarTempo(milissegundos) {
    if (milissegundos <= 0) {
        return "Tempo Esgotado!";
    } else {
        const segundos = Math.floor(milissegundos / 1000);
        const minutos = Math.floor(segundos / 60);
        const segundosRestantes = segundos % 60;
        return `${minutos.toString().padStart(2, "0")}:${segundosRestantes.toString().padStart(2, "0")}`;
    }
}

function exibirAlerta(mensagem) {
    const alerta = document.createElement("div");
    alerta.className = "alerta";
    alerta.textContent = mensagem;
    document.body.appendChild(alerta);
    setTimeout(() => alerta.remove(), 3000);
}

function removerTarefa(id) {
    fetch(`/tarefas/${id}`, {
        method: "DELETE"
    })
    .then(response => {
        if (response.ok) {
            tarefas = tarefas.filter(tarefa => tarefa.id !== id);
            renderizarTarefas();
        }
    })
    .catch(error => console.error("Erro ao remover tarefa:", error));
}