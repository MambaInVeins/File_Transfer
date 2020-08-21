from qiniu import Auth, put_data

'''
accessKey=qeg4bbEkVHLA5eAttv7L5HBeTQ5MtMBzaiU-LcI1
secretKey=Nvcak_xnLn2S1Z4UuXnwkZiAgqPSUUW5PucbYte9
bucket=huka
'''

access_key = 'qeg4bbEkVHLA5eAttv7L5HBeTQ5MtMBzaiU-LcI1'

secret_key = 'Nvcak_xnLn2S1Z4UuXnwkZiAgqPSUUW5PucbYte9'

# 空间名
bucket_name = 'huka'


def qiniu_upload_file(data):
    """
    上传文件
    :param data: 要上传的bytes类型数据
    :return:
    """
    # 创建鉴权对象
    q = Auth(access_key=access_key, secret_key=secret_key)

    # 生产token, 上传凭证
    token = q.upload_token(bucket=bucket_name)

    # 上传文件，None是文件名，指定None的话七牛云会自动生成一个文件名，也可以自己指定，但自己指定文件名时不能上传重复的文件
    ret, res = put_data(token, None, data=data)
    ret.get('key')

    print(ret)

    print(res)

    if res.status_code != 200:
        raise Exception("upload failed")
    return ret, res


