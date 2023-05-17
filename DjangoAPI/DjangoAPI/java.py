import bioformats as bf
import javabridge

def start_java():
    # Start CellProfiler's JVM via Javabridge   

    javabridge.start_vm(class_path=bf.JARS, max_heap_size='6G')
    javabridge.attach()
    
    # This is so that Javabridge doesn't spill out a lot of DEBUG messages during runtime. From CellProfiler/python-bioformats.
    rootLoggerName = javabridge.get_static_field("org/slf4j/Logger", "ROOT_LOGGER_NAME", "Ljava/lang/String;")
    rootLogger = javabridge.static_call("org/slf4j/LoggerFactory", "getLogger", "(Ljava/lang/String;)Lorg/slf4j/Logger;", rootLoggerName)
    logLevel = javabridge.get_static_field("ch/qos/logback/classic/Level", "WARN", "Lch/qos/logback/classic/Level;")
    javabridge.call(rootLogger, "setLevel", "(Lch/qos/logback/classic/Level;)V", logLevel)

def stop_java():
    javabridge.detach()
    javabridge.kill_vm()
