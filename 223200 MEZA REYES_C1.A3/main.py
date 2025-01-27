import sys
import traceback
import logging
from datetime import datetime
from pathlib import Path
from gui.app import App

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"app_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

def run_application():
    logger = setup_logging()
    logger.info("Iniciando aplicación")
    
    try:        
        app = App()
                
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            logger.error("Error no capturado:", exc_info=(exc_type, exc_value, exc_traceback))
        
        sys.excepthook = handle_exception
                
        logger.info("Aplicación configurada, iniciando mainloop")
        app.mainloop()
        
    except Exception as e:
        logger.error(f"Error al iniciar la aplicación: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        logger.info("Aplicación finalizada")

def main():
    try:
        run_application()
    except Exception as e:
        print(f"Error crítico: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()