var tarefas = JSON.parse(localStorage.getItem('tarefas')) || [];

function adicionarTarefa() {
    const nomeInput = document.getElementById('nomeTarefa');
    const duracaoInput = document.getElementById('duracaoTarefa');
    
    if (!nomeInput.value || !duracaoInput.value) {
        alert('Preencha os campos obrigatórios!');
        return;
    }

    const novaTarefa = {
        id: Date.now(),
        nome: nomeInput.value,
        descricao: document.getElementById('descricaoTarefa').value,
        duracao: parseInt(duracaoInput.value) * 60,
        dataCriacao: Date.now(),
        dataLimite: null,
        progresso: 0,
        expirada: false
    };

    novaTarefa.dataLimite = novaTarefa.dataCriacao + (novaTarefa.duracao * 1000);
    tarefas.push(novaTarefa);
    
    nomeInput.value = '';
    document.getElementById('descricaoTarefa').value = '';
    duracaoInput.value = '';
    
    salvarLocalStorage();
    renderizarTarefas(true);
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
    const container = document.getElementById('listaTarefas');
    container.innerHTML = '';
    
    tarefas.forEach(tarefa => {
        const elemento = document.createElement('div');
        elemento.id = `tarefa-${tarefa.id}`;
        elemento.className = `cartao-tarefa${novaAdicao ? ' nova' : ''}`;
        elemento.innerHTML = `
            <h3>${tarefa.nome}</h3>
            ${tarefa.descricao ? `<p>${tarefa.descricao}</p>` : ''}
            <div class="barra-progresso">
                <div class="progresso" style="width: ${Math.min(tarefa.progresso, 100)}%"></div>
            </div>
            <div class="contador-tempo">${formatarTempo(tarefa.dataLimite - Date.now())}</div>
            <button onclick="removerTarefa(${tarefa.id})">🗑️ Remover</button>
        `;
        
        if (tarefa.expirada) {
            elemento.classList.add('expirada');
        }
        
        container.appendChild(elemento);
    });
}

function formatarTempo(milissegundos) {
    if(milissegundos <= 0) //tempo esgotado
    { 
        return 'Tempo Esgotado!';
    }
    else { //tempo não esgotado
        const segundos = Math.floor(milissegundos / 1000);
        const minutos = Math.floor(segundos / 60);
        const segundosRestantes = segundos % 60;
        return `${minutos.toString().padStart(2, '0')}:${segundosRestantes.toString().padStart(2, '0')}`;
    }
}

function exibirAlerta(mensagem) {
    const alerta = document.createElement('div');
    alerta.className = 'alerta';
    alerta.textContent = mensagem;
    document.body.appendChild(alerta);
    
    setTimeout(() => {
        alerta.remove();
    }, 3000);
}

function removerTarefa(id) {
    const elemento = document.getElementById(`tarefa-${id}`);
    if(elemento) {
        elemento.style.opacity = '0';
        elemento.style.transform = 'translateY(-1rem)';
        setTimeout(() => elemento.remove(), 300);
    }
    tarefas = tarefas.filter(tarefa => tarefa.id !== id);
    salvarLocalStorage();
}

function salvarLocalStorage() {
    localStorage.setItem('tatefas', JSON.stringify(tarefas));
}

setInterval(atualizarTempo, 200); //200ms == 0.2s
renderizarTarefas();