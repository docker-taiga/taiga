#!/bin/env python3

import sys
import subprocess
import re



dockertaiga_images = [
  {'name': 'back', 'git': 'https://github.com/kaleidos-ventures/taiga-back'},
  {'name': 'front', 'git': 'https://github.com/kaleidos-ventures/taiga-front-dist'},
  {'name': 'events', 'git': 'https://github.com/kaleidos-ventures/taiga-events'},
  {'name': 'proxy'},
  {'name': 'rabbit'},
]



def last_releases(repo, count):
  res = subprocess.run(['git', 'ls-remote', '--tags', repo], stdout=subprocess.PIPE, check=True)
  if res.returncode != 0:
    return []
  refs = res.stdout.decode(sys.stdout.encoding).splitlines()
  tagre = re.compile(r'/(\d+\.\d+\.\d+).*$')
  tags = { m.group(1) for m in map(lambda r : tagre.search(r), refs) if m }
  return sorted(tags, reverse=True)[0:count]



def tag_releases(rels):
  rels.reverse()

  verlist = list(map(lambda x : tuple(map(lambda s : int(s), x.split('.'))), rels))
  verlist.sort()

  ver = {}
  for v in verlist:
    if not v[0] in ver:
      ver[v[0]] = {}
    if not v[1] in ver[v[0]]:
      ver[v[0]][v[1]] = []
    ver[v[0]][v[1]].append(v[2])

  res = { rel : [rel] for rel in rels }

  for vmaj in ver:
    for vmin in ver[vmaj]:
      patch = ver[vmaj][vmin][-1]
      vers = '{}.{}.{}'.format(vmaj, vmin, patch)
      res[vers].append('{}.{}'.format(vmaj, vmin))
    res[vers].append('{}'.format(vmaj))
  res[vers].append('latest')

  res = [ {'release': k, 'tags': res[k]} for k in res ]
  return res



def build_image(image_name):
  image = 'dockertaiga/' + image_name
  subprocess.run(['docker', 'build',
    '-t', image,
    image_name,
  ])
  return image



def build_images(image_name, repo, releases):
  image = 'dockertaiga/' + image_name
  images = []
  for rel in releases:
    subprocess.run(['docker', 'build',
      '-t', '{}:{}'.format(image, rel['release']),
      '--build-arg', 'REPO={}'.format(repo),
      '--build-arg', 'VERSION={}'.format(rel['release']),
      image_name,
    ])
    for tag in rel['tags']:
      if tag != rel['release']:
        subprocess.run(['docker', 'tag',
          '{}:{}'.format(image, rel['release']),
          '{}:{}'.format(image, tag),
        ])
        images.append('{}:{}'.format(image, tag))
  return images



def push_images(images):
  for image in images:
    subprocess.run(['docker', 'push', image])



if __name__ == "__main__":
  images = []
  for img in dockertaiga_images:
    if 'git' in img:
      rels = last_releases(img['git'], 3)
      rels = tag_releases(rels)
      built_images = build_images(img['name'], img['git'], rels)
      images.extend(built_images)
    else:
      built_image = build_image(img['name'])
      images.append(built_image)
  push_images(images)
  print('\n\n\nBuilt images:\n' + '\n'.join(images))
