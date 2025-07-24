pipeline {
    agent any

    stages {
        stage('Setup Python Environment') {
            steps {
                // Шаг создания виртуального окружения
                sh 'python3 -m venv venv'

                // Установка зависимостей из requirements.txt с флагом для обхода ограничений
                sh './venv/bin/pip install --break-system-packages -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Запуск тестов и генерация отчета allure
                sh './venv/bin/python -m pytest --alluredir allure-results'
            }
        }

        stage('Generate Allure Report') {
            steps {
                // Публикация Allure отчетов (если установлен плагин Allure)
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            // Сохранение отчетов о тестировании и любых других артефактов
            archiveArtifacts artifacts: '**/allure-results/**', allowEmptyArchive: true
        }
        failure {
            // Если сборка провалилась, отправить уведомление или выполнить другое действие
            echo 'The build failed!'
        }
    }
}
