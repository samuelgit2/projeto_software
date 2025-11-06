from models import db, Task
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

# Cria a aplicação Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha-chave-secreta-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o banco de dados com o app
db.init_app(app)

# Página principal - mostra o Kanban
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Criar nova tarefa
@app.route('/task', methods=['POST'])
def create_task():
    try:
        title = request.form.get('title')
        description = request.form.get('description', '')
        priority = request.form.get('priority', 'Medium')
        
        new_task = Task(
            title=title,
            description=description,
            priority=priority
        )
        
        db.session.add(new_task)
        db.session.commit()
        
        flash('Tarefa criada com sucesso!', 'success')
    except Exception as e:
        flash('Erro ao criar tarefa', 'error')
    
    return redirect(url_for('index'))

# Excluir tarefa
@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Tarefa excluída com sucesso!'})
    except Exception as e:
        return jsonify({'error': 'Erro ao excluir tarefa'}), 500
    
# Mudar estado das tarefas (mover entre colunas)
@app.route('/task/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    try:
        task = Task.query.get_or_404(task_id)
        new_status = request.json.get('status')
        
        if new_status in ['To Do', 'In Progress', 'Done']:
            task.status = new_status
            db.session.commit()
            return jsonify({'message': f'Tarefa movida para {new_status}!'})
        else:
            return jsonify({'error': 'Status inválido'}), 400
            
    except Exception as e:
        print(f"Erro ao atualizar tarefa: {e}")
        return jsonify({'error': 'Erro ao atualizar tarefa'}), 500

# Executar a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("🎯 Servidor flask rodando em: http://localhost:5000")
    app.run(debug=True)