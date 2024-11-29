import { defineStore } from 'pinia';

export const useDataModelFormStore = defineStore('form', {
    state: (): Api.SystemManage.DataModelForm => ({
        currentStep: 1,
        stepOne: {
            database: null,
            tableName: null,
        },
        stepTwo: {
            fieldConf: null
        },
        stepThree: {
            dataModelName: null,
            dataModelDesc: null,
            dataDomain: null,
            topicDomain: null,
            status: null
        }
    }),

    actions: {
        nextStep() {
            if (this.currentStep < 3) {
                this.currentStep++;
            }
        },
        prevStep() {
            if (this.currentStep > 1) {
                this.currentStep--;
            }
        },
        setStep(step: number) {
            this.currentStep = step;
        },
        resetStore() {
            this.$reset()
        },
        updateFormData(rowData: any) {
            this.stepOne.database = rowData.database
            this.stepOne.tableName = rowData.tableName
            this.stepTwo.fieldConf = rowData.fieldConf
            this.stepThree.dataModelName = rowData.dataModelName
            this.stepThree.dataModelDesc = rowData.dataModelDesc
            this.stepThree.dataDomain = rowData.dataDomain
            this.stepThree.topicDomain = rowData.topicDomain
            this.stepThree.status = rowData.status
        }
    }
});