import pytube

url = input('https://www.youtube.com/watch?v=a-A2zQu_xpM')
yt = pytube.YouTube(url)
yt.streams.first().download()
print('Downloading video', url)
