import gradio as gr
import function as func


with gr.Blocks() as tab1: 
    gr.Markdown("## Загрузите файл и нажмите 'Отправить'")
    
    with gr.Row():
        with gr.Column():
            lang_radio = gr.Radio(
                choices=["English", "Русский"],
                label="Язык",  
                value="English"  # Значение по умолчанию
            )
            
            file_input = gr.File(label="Файл", file_types=[".png", ".jpg", ".jpeg", ".txt"])
            
            submit_button = gr.Button("Отправить")
        
        with gr.Column():
            output_text = gr.Textbox(label="Ответ от сервера", lines=10)
    
    submit_button.click(
        fn=func.send_file_to_backend, 
        inputs=[file_input, lang_radio],
        outputs=output_text,
    )

with gr.Blocks() as tab2:
    gr.Markdown("## Таблица обработанных файлов")
    
    show_button = gr.Button("ОБНОВИТЬ ДАННЫЕ")
    
    table = gr.Dataframe(
        headers=["ID", "Имя файла", "Дата и Время загрузки", "Описание", "Статус"], 
        col_count=5, 
        interactive=False  # Таблица только для чтения
    )
    show_button.click(
        fn=func.get_table_data,
        outputs=table
    )

iface = gr.TabbedInterface([tab1, tab2], ["Обработать файл", "Посмотреть обработанные файлы"])
