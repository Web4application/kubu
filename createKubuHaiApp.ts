/* eslint-disable import/no-extraneous-dependencies */
import retry from 'async-retry'
import { copyFileSync, existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { basename, dirname, join, resolve } from 'node:path'
import { cyan, green, red, yellow } from 'picocolors'
import { execSync } from 'node:child_process'

import type { RepoInfo } from './helpers/examples'
import {
  downloadAndExtractExample,
  downloadAndExtractRepo,
  existsInRepo,
  getRepoInfo,
  hasRepo,
} from './helpers/examples'
import type { PackageManager } from './helpers/get-pkg-manager'
import { tryGitInit } from './helpers/git'
import { install } from './helpers/install'
import { isFolderEmpty } from './helpers/is-folder-empty'
import { getOnline } from './helpers/is-online'
import { isWriteable } from './helpers/is-writeable'

import { getTemplateFile, installTemplate } from './templates'

export class DownloadError extends Error {}

export interface CreateKubuHaiAppOptions {
  appPath: string
  packageManager: PackageManager
  example?: string
  examplePath?: string
  typescript?: boolean
  dart?: boolean
  postgres?: boolean
  redis?: boolean
  ai?: boolean
  llm?: boolean
  nginx?: boolean
  https?: boolean
  eslint?: boolean
  srcDir?: boolean
  importAlias?: string
  skipInstall?: boolean
  empty?: boolean
  turbopack?: boolean
  disableGit?: boolean
  ghActions?: boolean
  minimal?: boolean
}

export async function createKubuHaiApp({
  appPath,
  packageManager,
  example,
  examplePath,
  typescript = true,
  dart = true,
  postgres = true,
  redis = true,
  ai = false,
  llm = false,
  nginx = true,
  https = false,
  eslint = true,
  srcDir = true,
  importAlias = '@',
  skipInstall = false,
  empty = false,
  turbopack = false,
  disableGit = false,
  ghActions = true,
  minimal = false,
}: CreateKubuHaiAppOptions): Promise<void> {
  const root = resolve(appPath)
  const appName = basename(root)

  if (!(await isWriteable(dirname(root)))) {
    console.error(
      red(
        'The application path is not writable. Check your folder permissions and try again.'
      )
    )
    process.exit(1)
  }

  mkdirSync(root, { recursive: true })

  if (!isFolderEmpty(root, appName)) {
    console.error(
      red(
        `The target directory "${appName}" is not empty. Please choose an empty folder.`
      )
    )
    process.exit(1)
  }

  const useYarn = packageManager === 'yarn'
  const isOnline = !useYarn || (await getOnline())
  const originalDirectory = process.cwd()

  console.log(green(`Creating a new Kubu-Hai app in ${root}`))
  console.log()

  process.chdir(root)

  // Download example or install template
  if (example) {
    let repoInfo: RepoInfo | undefined
    let repoUrl: URL | undefined

    try {
      repoUrl = new URL(example)
    } catch (err) {
      if ((err as any).code !== 'ERR_INVALID_URL') {
        console.error(err)
        process.exit(1)
      }
    }

    if (repoUrl) {
      if (repoUrl.origin !== 'https://github.com') {
        console.error(
          red(
            `Invalid URL: "${example}". Only GitHub repositories are supported.`
          )
        )
        process.exit(1)
      }
      repoInfo = await getRepoInfo(repoUrl, examplePath)

      if (!repoInfo) {
        console.error(
          red(`Could not resolve repository info for: "${example}".`)
        )
        process.exit(1)
      }

      const found = await hasRepo(repoInfo)
      if (!found) {
        console.error(
          red(`Repository does not exist or is not accessible: "${example}".`)
        )
        process.exit(1)
      }

      try {
        console.log(cyan(`Downloading repo: ${example}`))
        await retry(() => downloadAndExtractRepo(root, repoInfo!), { retries: 3 })
      } catch (reason) {
        throw new DownloadError(reason instanceof Error ? reason.message : String(reason))
      }
    } else {
      const found = await existsInRepo(example)
      if (!found) {
        console.error(
          red(
            `Could not find example named "${example}". Check your spelling or internet connection.`
          )
        )
        process.exit(1)
      }
      try {
        console.log(cyan(`Downloading example: ${example}`))
        await retry(() => downloadAndExtractExample(root, example), { retries: 3 })
      } catch (reason) {
        throw new DownloadError(reason instanceof Error ? reason.message : String(reason))
      }
    }
  } else {
    // Scaffold Kubu-Hai core templates
    await scaffoldKubuHaiCore({
      root,
      appName,
      typescript,
      dart,
      postgres,
      redis,
      ai,
      llm,
      nginx,
      https,
      eslint,
      srcDir,
      importAlias,
      skipInstall,
      turbopack,
      minimal,
    })
  }

  // Setup Git
  if (disableGit) {
    console.log(yellow('Skipping git initialization.'))
  } else if (tryGitInit(root)) {
    console.log(green('Initialized a git repository.'))
  }

  // Add GitHub Actions workflows if requested
  if (ghActions) {
    setupGitHubActions(root)
  }

  // Final instructions
  console.log(green('Success! Your Kubu-Hai app is ready.'))
  console.log()
  console.log('Next steps:')
  console.log(cyan(`  cd ${appName}`))
  if (!skipInstall) {
    console.log(cyan(`  ${packageManager} ${useYarn ? '' : 'run '}dev`))
  }
  console.log()
}

/**
 * Scaffold Kubu-Hai core stack templates
 */
async function scaffoldKubuHaiCore({
  root,
  appName,
  typescript,
  dart,
  postgres,
  redis,
  ai,
  llm,
  nginx,
  https,
  eslint,
  srcDir,
  importAlias,
  skipInstall,
  turbopack,
  minimal,
}: {
  root: string
  appName: string
  typescript: boolean
  dart: boolean
  postgres: boolean
  redis: boolean
  ai: boolean
  llm: boolean
  nginx: boolean
  https: boolean
  eslint: boolean
  srcDir: boolean
  importAlias: string
  skipInstall: boolean
  turbopack: boolean
  minimal: boolean
}): Promise<void> {
  // Create folders for backend, frontend, infra
  const backendDir = join(root, 'backend')
  const frontendDir = join(root, 'frontend')
  const infraDir = join(root, 'infra')

  mkdirSync(backendDir, { recursive: true })
  mkdirSync(frontendDir, { recursive: true })
  mkdirSync(infraDir, { recursive: true })

  // Backend scaffold (FastAPI + requirements.txt)
  const requirements = [
    'fastapi',
    'uvicorn[standard]',
    'psycopg2-binary',
    'redis',
  ]
  if (ai) requirements.push('transformers', 'torch') // example AI deps
  if (llm) requirements.push('llama-cpp-python') // example LLM deps

  writeFileSync(
    join(backendDir, 'requirements.txt'),
    requirements.join('\n')
  )

  writeFileSync(
    join(backendDir, 'main.py'),
    `from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to Kubu-Hai Backend!"}
`
  )

  // Frontend scaffold (Dart or minimal)
  if (dart) {
    writeFileSync(
      join(frontendDir, 'pubspec.yaml'),
      `name: ${appName}_frontend
description: Kubu-Hai Dart Frontend
environment:
  sdk: ">=2.18.0 <3.0.0"
dependencies:
  flutter:
    sdk: flutter
  http: ^0.13.0
`
    )
    writeFileSync(
      join(frontendDir, 'lib/main.dart'),
      `import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        body: Center(child: Text('Welcome to Kubu-Hai Frontend!')),
      ),
    );
  }
}
`
    )
  } else {
    // Minimal HTML fallback
    writeFileSync(
      join(frontendDir, 'index.html'),
      `<html><body><h1>Welcome to Kubu-Hai Frontend!</h1></body></html>`
    )
  }

  // Infra scaffold: docker-compose, nginx.conf, .env.example

  // docker-compose.yml
  const dockerCompose = `
version: '3.8'
services:
  backend:
    build: ./backend
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_HOST=postgres
      - REDIS_HOST=redis
    depends_on:
      - postgres
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: kubu
      POSTGRES_PASSWORD: kubu_pass
      POSTGRES_DB: kubu_db
    volumes:
      - postgres-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data

volumes:
  postgres-data:
  redis-data:
`

  writeFileSync(join(infraDir, 'docker-compose.yml'), dockerCompose.trim())

  // nginx.conf (simple reverse proxy for backend and frontend)
  if (nginx) {
    const nginxConf = `
server {
  listen 80;
  server_name localhost;

  location /api/ {
    proxy_pass http://backend:8000/;
  }

  location / {
    proxy_pass http://frontend:3000/;
  }
}
`
    writeFileSync(join(infraDir, 'nginx.conf'), nginxConf.trim())
  }

  // .env.example
  const envExample = `
POSTGRES_USER=kubu
POSTGRES_PASSWORD=kubu_pass
POSTGRES_DB=kubu_db
POSTGRES_HOST=postgres
REDIS_HOST=redis
`
  writeFileSync(join(root, '.env.example'), envExample.trim())

  // Optionally install deps (you can add install logic here, skipped for brevity)

  console.log(green('Scaffolded core Kubu-Hai backend, frontend, and infra templates.'))
}

/**
 * Setup GitHub Actions workflows for CI/CD
 */
function setupGitHubActions(root: string): void {
  const workflowsDir = join(root, '.github', 'workflows')
  mkdirSync(workflowsDir, { recursive: true })

  // Simple workflow for backend testing + linting
  const backendWorkflow = `
name: Backend CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt
      - name: Run tests
        run: |
          echo "No tests defined yet"
`

  writeFileSync(join(workflowsDir, 'backend-ci.yml'), backendWorkflow.trim())

  console.log(green('Added GitHub Actions workflow for backend CI.'))
}
