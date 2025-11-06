from src.models import db, Task
from flask import Flask, render_template, request, redirect, url_for, flash

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

# Executar a aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("🎯 Servidor flask rodando em: http://localhost:5000")
    app.run(debug=True)