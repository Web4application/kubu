cronitor.wrap('important-background-job', function () {
    console.log('running background job with monitoring!');
});

// Or, embed telemetry events directly in your code.
const monitor = new cronitor.Monitor('important-background-job');

// the job has started
monitor.ping({state: 'run'});

// the job has completed successfully
monitor.ping({state: 'complete'});

// the job has failed
monitor.ping({state: 'fail'});
