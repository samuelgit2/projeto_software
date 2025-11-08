import pytest
import os
import sys

# Adiciona o diretório src ao path para importar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import app, db, Task

@pytest.fixture
def client():
    """Configura o app para testes"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_task(client):
    """Testa a criação de uma tarefa"""
    with app.app_context():
        task = Task(
            title="Tarefa de Teste",
            description="Descrição da tarefa de teste",
            priority="High"
        )
        db.session.add(task)
        db.session.commit()
        
        # Verifica se a tarefa foi criada
        assert task.id is not None
        assert task.title == "Tarefa de Teste"
        assert task.status == "To Do"  # Valor padrão

def test_task_priorities(client):
    """Testa as prioridades das tarefas"""
    with app.app_context():
        task_low = Task(title="Tarefa Baixa", priority="Low")
        task_medium = Task(title="Tarefa Média", priority="Medium")
        task_high = Task(title="Tarefa Alta", priority="High")
        task_critical = Task(title="Tarefa Crítica", priority="Critical")
        
        assert task_low.priority == "Low"
        assert task_medium.priority == "Medium"
        assert task_high.priority == "High"
        assert task_critical.priority == "Critical"

def test_home_page(client):
    """Testa se a página inicial carrega corretamente"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'TechFlow Task Manager' in response.data

def test_create_task_via_form(client):
    """Testa a criação de tarefa via formulário"""
    response = client.post('/task', data={
        'title': 'Nova Tarefa via Teste',
        'description': 'Descrição do teste',
        'priority': 'Medium'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Nova Tarefa via Teste' in response.data