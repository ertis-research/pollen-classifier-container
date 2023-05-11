import bioformats
import javabridge

jars_venv_PATH = ['C:\\Users\\ANTONI~1\\Trabajo\\LifeWatch\\Polen\\userTeamAngularTest\\myenv\\Lib\\site-packages\\javabridge\\jars\\rhino-1.7R4.jar', 'C:\\Users\\ANTONI~1\\Trabajo\\LifeWatch\\Polen\\userTeamAngularTest\\myenv\\Lib\\site-packages\\javabridge\\jars\\runnablequeue.jar', 'C:\\Users\\ANTONI~1\\Trabajo\\LifeWatch\\Polen\\userTeamAngularTest\\myenv\\Lib\\site-packages\\javabridge\\jars\\cpython.jar', 'C:\\Users\\ANTONI~1\\Trabajo\\LifeWatch\\Polen\\userTeamAngularTest\\myenv\\Lib\\site-packages\\bioformats\\jars\\bioformats_package.jar']

def start_java():
    # Start CellProfiler's JVM via Javabridge   

    javabridge.start_vm(class_path=bioformats.JARS, max_heap_size='6G') # Sobremesa "ps3aj"
    # javabridge.start_vm(class_path=jars_venv_PATH, max_heap_size='6G') # Laptop "Poblema de las tildes y/o el espacio" "Antonio Jesús"
    javabridge.attach()
    

    # This is so that Javabridge doesn't spill out a lot of DEBUG messages during runtime. From CellProfiler/python-bioformats.
    rootLoggerName = javabridge.get_static_field("org/slf4j/Logger", "ROOT_LOGGER_NAME", "Ljava/lang/String;")
    rootLogger = javabridge.static_call("org/slf4j/LoggerFactory", "getLogger", "(Ljava/lang/String;)Lorg/slf4j/Logger;", rootLoggerName)
    logLevel = javabridge.get_static_field("ch/qos/logback/classic/Level", "WARN", "Lch/qos/logback/classic/Level;")
    javabridge.call(rootLogger, "setLevel", "(Lch/qos/logback/classic/Level;)V", logLevel)

def stop_java():
    javabridge.detach()
    javabridge.kill_vm()
