import { RptClient } from '@sap-ai-sdk/rpt'
import type { RPT1Payload } from './types.js'

/**
 * Client for interacting with the RPT-1 model using SAP AI SDK
 * The SDK handles OAuth authentication and API communication automatically
 */
export class RPT1Client {
    private client: RptClient

    constructor(modelName: 'sap-rpt-1-small' | 'sap-rpt-1-large' = 'sap-rpt-1-small') {
        // Initialize the SDK client
        // By default, it uses 'sap-rpt-1-small'
        this.client = new RptClient(modelName)
    }

    /**
     * Make prediction request using the SDK's predictWithoutSchema method
     * The schema will be inferred from the data
     */
    async predictWithoutSchema(payload: RPT1Payload): Promise<any> {
        try {
            const prediction = await this.client.predictWithoutSchema(payload as any)
            return prediction
        } catch (error) {
            throw new Error(`RPT-1 prediction failed: ${error instanceof Error ? error.message : String(error)}`)
        }
    }
}
