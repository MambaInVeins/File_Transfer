C语言字符串替换函数(strrpl)

    #include<stdio.h>
    #include<string.h>

    // 参数说明:in，源字符串;out,存放最后结果的字符串;outlen，out最大的大小;src，要替换的字符串;dst，替换成什么字符串
    char *strrpl(char *in, char *out, int outlen, const char *src, char *dst)
    {
        char *p = in;
        unsigned int  len = outlen - 1;

        // 这几段检查参数合法性
        if((NULL == src) || (NULL == dst) || (NULL == in) || (NULL == out))
        {
            return NULL;
        }
        if((strcmp(in, "") == 0) || (strcmp(src, "") == 0))
        {
            return NULL;
        }
        if(outlen <= 0)
        {
            return NULL;
        }

        while((*p != '\0') && (len > 0))
        {
            if(strncmp(p, src, strlen(src)) != 0)
            {
                int n = strlen(out);

                out[n] = *p;
                out[n + 1] = '\0';

                p++;
                len--;
            }
            else
            {
                strcat(out,dst);
                p += strlen(src);
                len -= strlen(dst);
            }
        }

        return out;
    }

    int main(){
        char *sStr = "123&amp;";
        char *sMatchStr = "&amp;";
        char *sReplaceStr = "&";
        char out[100];
        memset(out,0,100);
        strrpl(sStr,out,100,sMatchStr,sReplaceStr);
        printf("out:%s\n",out);
    }