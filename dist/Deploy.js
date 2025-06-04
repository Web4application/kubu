const core = require('@actions/core')
const exec = require('@actions/exec')
const getContext = require('./context')

async function deploy() {
  try {
    const ctx = getContext()
    core.info(`Starting deployment for artifact: ${ctx.artifactName}`)

    // Checkout the gh-pages branch or create it if it doesn't exist
    await exec.exec('git', ['fetch', 'origin', 'gh-pages'])
    const result = await exec.exec('git', ['checkout', 'gh-pages'], {ignoreReturnCode: true})

    if (result !== 0) {
      core.info('gh-pages branch does not exist. Creating new orphan branch.')
      await exec.exec('git', ['checkout', '--orphan', 'gh-pages'])
      await exec.exec('git', ['rm', '-rf', '.'])
      await exec.exec('git', ['commit', '--allow-empty', '-m', 'Initial gh-pages commit'])
      await exec.exec('git', ['push', '-u', 'origin', 'gh-pages'])
    }

    // Clean existing files
    await exec.exec('git', ['rm', '-rf', '.'])
    
    // Extract artifact contents - assuming it’s in ./artifact folder after download
    // You’ll need to download the artifact prior to this (this script assumes it's done)
    // For example, if your build outputs to ./dist:
    await exec.exec('cp', ['-r', './dist/.', './'])

    await exec.exec('git', ['add', '.'])
    await exec.exec('git', ['commit', '-m', `Deploy ${ctx.buildVersion}`])

    // Push to gh-pages branch
    await exec.exec('git', ['push', 'origin', 'gh-pages', '--force'])

    core.info('Deployment completed successfully! 🎉')
  } catch (error) {
    core.setFailed(`Deployment failed: ${error.message}`)
  }
}

deploy()
