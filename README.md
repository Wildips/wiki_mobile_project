# Проект по тестированию мобильного приложения на примере 

> <a target="_blank" href="https://github.com/wikimedia/apps-android-wikipedia/releases">wikipedia</a>

#### Список проверок, реализованных в авто-тестах

- [x] Поиск требуемого результата
- [x] Поиск и переход по результатам поиска
- [x] Настройка аккаунта при первом входе

#### Параметры сборки

* `ENVIRONMENT` - параметр определяет окружение для запуска тестов, по умолчанию STAGE
* `COMMENT` - комментарий к сборке

### Для запуска авто-тестов в Jenkins

#### 1. Открыть <a target="_blank" href="https://jenkins.autotests.cloud/job/125_mobile_tests/">проект</a>

![This is an image](/images/jenkins_project_main.png)

#### 2. Выбрать пункт **Build with Parameters**

#### 3. Внести изменения в конфигурации сборки, при необходимости

#### 4. Нажать **Build**

#### 5. Результат запуска сборки можно посмотреть как в классическом формате Allure Results

![This is an image](/images/allure_example.png)

#### 6. Так и в интегрированном с Jira и Allure TestOps

![This is an image](/images/testops_example.png)

#### 7. Информация о завершении сборки так же будет опубликована в telegram на канале

![This is an image](/images/notification_example.png)

#### 8. Запуск авто-тестов

Пример командной строки:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -vv -l -s . --context=$CONTEXT 
```
* '--context' не обязательный параметр имеющий значение по умолчанию<br/> 
"bstack". Для локального запуска тестов должен иметь значение "local_emulator"

Создание локального отчета:

```bash
allure serve allure-results
```

## Пример выполнения удаленного теста

![This is an video](/images/demo_test_execution.gif)


#### 9. Так же результаты выполнения будут транслированы в Jira

![This is an image](/images/jira_integration.png)