import 'dotenv/config'
import { InvestigationWorkflow } from './investigationWorkflow.js'
import { payload } from './payload.js'

/**
 * Main entry point for the Investigator Workflow system
 * Orchestrates a multi-agent investigation to solve an art theft case
 */
async function main() {
    try {
        console.log('═══════════════════════════════════════════════════════════')
        console.log('   🔍 ART THEFT INVESTIGATION - MULTI-AGENT SYSTEM')
        console.log('═══════════════════════════════════════════════════════════\n')

        // Initialize the investigator workflow
        const workflow = new InvestigationWorkflow(process.env.MODEL_NAME!)

        // Define the suspects
        const suspectNames = 'Sophie Dubois, Marcus Chen, Viktor Petrov'

        console.log('📋 Case Details:')
        console.log(`   • Stolen Items: ${payload.rows.length} artworks`)
        console.log(`   • Suspects: ${suspectNames}`)
        console.log(`   • Investigation Team: 3 specialized agents\n`)

        // Start the investigation
        const startTime = Date.now()

        const result = await workflow.kickoff({
            payload,
            suspect_names: suspectNames,
        })

        const duration = ((Date.now() - startTime) / 1000).toFixed(2)

        console.log('\n═══════════════════════════════════════════════════════════')
        console.log('   📘 FINAL INVESTIGATION REPORT')
        console.log('═══════════════════════════════════════════════════════════\n')
        console.log(result)
        console.log('\n═══════════════════════════════════════════════════════════')
        console.log(`   ⏱️  Investigation completed in ${duration} seconds`)
        console.log('═══════════════════════════════════════════════════════════\n')
    } catch (error) {
        console.error('\n❌ Investigation failed with error:')
        console.error(error)
        process.exit(1)
    }
}

// Run the main function
main()
