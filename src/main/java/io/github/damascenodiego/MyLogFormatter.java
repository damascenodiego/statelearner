package io.github.damascenodiego;

import java.util.Date;
import java.util.logging.LogRecord;
import java.util.logging.SimpleFormatter;

public class MyLogFormatter extends SimpleFormatter {
    private static final String format = "[%1$tY-%1$tm-%1$td %1$tH:%1$tM:%1$tS.%1$tL] [%2$s] %3$s %n";

    @Override
    public synchronized String format(LogRecord lr) {
        return String.format(format,
                new Date(lr.getMillis()),
                lr.getLevel().getLocalizedName(),
                lr.getMessage()
        );
    }
}