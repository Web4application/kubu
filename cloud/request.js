addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
    const url = new URL(request.url)
    
    if (url.pathname === '/predict') {
        const data = await request.json()  // Get prediction data from client
        
        // Here, you can add logic to forward the request to your backend server
        const response = await fetch('https://your-backend-url/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        })
        
        const prediction = await response.json()
        
        // Return the AI prediction as a response
        return new Response(JSON.stringify(prediction), { 
            status: 200, 
            headers: { 'Content-Type': 'application/json' }
        })
    }

    return new Response("Not Found", { status: 404 })
}
