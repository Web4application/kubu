// builder-registry.ts
import { Builder } from '@builder.io/react'

Builder.registerComponent(
  dynamic(() => import('./components/heading')),
  {
    name: 'Heading',
    inputs: [{ name: 'kubu-hai', type: 'text' }],
    image: 'https://cdn.builder.io/api/v1/image/assets%2FYJIGb4i01jvw0SRdL5Bt%2F6bef27ee40d24f3b88239fd7e616f82a'
  }
)
