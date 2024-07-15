#include <stdlib.h>
#include <errno.h>
#include <string.h>

#include "logging.h"

char *read_file(char *filepath)
{
    if (NULL == filepath)
    {
        ELOG("Provided filepath is null\n");
        return NULL;
    }

    DLOG("Opening %s\n", filepath);
    FILE *fp = fopen(filepath, "r");
    if (NULL == fp)
    {
        ELOG("Failed to open %s\n", filepath);
        return NULL;
    }

    DLOG("Opened %s, getting file size\n", filepath);

    fseek(fp, 0L, SEEK_END);
    long f_size = ftell(fp);
    fseek(fp, 0L, SEEK_SET);

    DLOG("File size is %ld, allocating buffer\n", f_size);

    char *buff = malloc(f_size + 1);
    if (NULL == buff)
    {
        ELOG("Failed to allocate memory to read /etc/os-release\n");
        fclose(fp);
        return NULL;
    }
    buff[f_size] = '\0';

    DLOG("Buffer allocated, reading file\n");

    size_t amt_read = 0;
    do
    {
        amt_read = fread(buff, sizeof(char), f_size, fp);
        DLOG("Read %ld bytes, errno: %d:%s\n", amt_read, errno, strerror(errno));
        if (feof(fp))
        {
            DLOG("End of file reached\n");
            break;
        }
        if (ferror(fp))
        {
            ELOG("There was an error reading %s: %d:%s", filepath, errno, strerror(errno));
            fclose(fp);
            return NULL;
        }
    } while (amt_read > 0);

    DLOG("Finished reading, closing file\n");

    fclose(fp);
    DLOG("Closed, returning buffer.\n");
    return buff;
}