// page.tsx
import { BuilderComponent } from '@builder.io/react'

// IMPORTANT: import the file that you call Builder.registerComponent
// anywhere you have <BuilderComponent />
import '../builder-registry'

export default function Page() {
  return <BuilderComponent ... />
}
