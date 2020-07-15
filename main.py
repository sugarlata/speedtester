import datetime
import speedtest

from ftplib import FTP

from config import FTP_CREDS
FILENAME = 'speeds.csv'

def main():
    now = datetime.datetime.now()
    now = now.strftime('%Y/%m/%d %H:%M')
    st = speedtest.Speedtest()

    st.get_best_server()

    dl_speed = st.download()
    ul_speed = st.upload()

    pg_speed = st.results.ping

    with open(FILENAME, 'a+') as f:
        f.writelines([','.join([
        now,
        str(dl_speed / (1024**2)),
        str(ul_speed / (1024**2)),
        str(pg_speed)
        ]), '\n'])

    try:
        upload(FILENAME)
    except Exception as e:
        print(e)


def upload(filename):

    with FTP(host='192.168.5.215') as ftp:
        ftp.login(FTP_CREDS['user'], FTP_CREDS['pass'])
        ftp.cwd('/Volumes/SW/speedtest')

        f = open(filename, 'rb')
        ftp.storbinary('STOR %s' % filename, f)
        f.close()

if __name__ == '__main__':
    main()


