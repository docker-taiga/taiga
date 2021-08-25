#!/bin/env python3

import sys
import argparse
import subprocess
import re



dockertaiga_images = [
  {'name': 'back', 'git': 'https://github.com/kaleidos-ventures/taiga-back'},
  {'name': 'front', 'git': 'https://github.com/kaleidos-ventures/taiga-front-dist'},
  {'name': 'events', 'git': 'https://github.com/kaleidos-ventures/taiga-events'},
  {'name': 'proxy'},
  {'name': 'rabbit'},
]



def main():
  image_names = [ img['name'] for img in dockertaiga_images ]
  ap = argparse.ArgumentParser(description='builds, tags and pushes recent releases of taiga')
  ap.add_argument('-r', '--releases', type=int, default=1, help='number of recent releases to build')
  ap.add_argument('-i', '--images', choices=image_names, nargs='*', help='names of the images to build')
  ap.add_argument('-p', '--push', action='store_true', help='push built images to dockerhub')
  ap.add_argument('-y', '--non-interactive', action='store_true', help='skip confirmation prompts')
  ap.add_argument('-n', '--dry-run', action='store_true', help='perform a dry run')
  args = ap.parse_args(sys.argv[1:])

  if args.images is None:
    images_to_build = dockertaiga_images
  else:
    images_to_build = [ img for img in dockertaiga_images if img['name'] in args.images ]

  print('images to build:')
  for img in images_to_build:
    if 'git' in img:
      rels = last_releases(img['git'], args.releases)
      img['rels'] = tag_releases(rels)
      for rel in img['rels']:
        print('\tdockertaiga/{} ({})'.format(img['name'], ', '.join(rel['tags'])))
    else:
      print('\tdockertaiga/{}'.format(img['name']))
  print('\n')

  if not args.non_interactive:
    sys.stdout.write('continue build? [Y/n]: ')
    choice = input().lower()
    if choice == '':
      choice = 'y'
    if choice in ['n', 'no']:
      return

  built_images = []

  for img in images_to_build:
    if 'git' in img:
      images = build_images(img['name'], img['git'], img['rels'], args.dry_run)
      built_images.extend(images)
    else:
      image = build_image(img['name'], args.dry_run)
      built_images.append(image)

  print('\nbuilt images:')
  for img in built_images:
    print('\t{}'.format(img))
  print('\n')

  if args.push:
    if not args.non_interactive:
      sys.stdout.write('push images? [Y/n]: ')
      choice = input().lower()
      if choice == '':
        choice = 'y'
      if choice in ['n', 'no']:
        return
    push_images(built_images, args.dry_run)



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



def build_image(image_name, dry_run=False):
  image = 'dockertaiga/' + image_name
  print('\nBUILDING {}\n'.format(image))
  if not dry_run:
    subprocess.run(['docker', 'build',
      '-t', image,
      image_name,
    ])
  return image



def build_images(image_name, repo, releases, dry_run=False):
  image = 'dockertaiga/' + image_name
  images = []
  for rel in releases:
    print('\nBUILDING {}:{}\n'.format(image, rel['release']))
    if not dry_run:
      subprocess.run(['docker', 'build',
        '-t', '{}:{}'.format(image, rel['release']),
        '--build-arg', 'REPO={}'.format(repo),
        '--build-arg', 'VERSION={}'.format(rel['release']),
        image_name,
      ])
    for tag in rel['tags']:
      if tag != rel['release']:
        if not dry_run:
          subprocess.run(['docker', 'tag',
            '{}:{}'.format(image, rel['release']),
            '{}:{}'.format(image, tag),
          ])
      images.append('{}:{}'.format(image, tag))
  return images



def push_images(images, dry_run=False):
  for image in images:
    print('\nPUSHING {}\n'.format(image))
    if not dry_run:
      subprocess.run(['docker', 'push', image])



if __name__ == "__main__":
  main()
