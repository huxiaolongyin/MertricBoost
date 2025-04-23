import { defineStore } from 'pinia';

export const useDataModelFormStore = defineStore('form', {
  state: (): Api.SystemManage.DataModelForm => ({
    currentStep: 1,
    stepOne: {
      databaseId: null,
      tableName: null
    },
    stepTwo: {
      columnsConf: null
    },
    stepThree: {
      name: null,
      description: null,
      dataDomains: null,
      topicDomains: null,
      status: null
    }
  }),

  actions: {
    nextStep() {
      if (this.currentStep < 3) {
        this.currentStep += 1;
      }
    },
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep -= 1;
      }
    },
    setStep(step: number) {
      this.currentStep = step;
    },
    resetStore() {
      this.$reset();
    },
    updateFormData(rowData: any) {
      this.stepOne.databaseId = rowData.databaseId;
      this.stepOne.tableName = rowData.tableName;
      this.stepTwo.columnsConf = rowData.columnsConf;
      this.stepThree.name = rowData.name;
      this.stepThree.description = rowData.description;
      this.stepThree.dataDomains = rowData.dataDomains;
      this.stepThree.topicDomains = rowData.topicDomains;
      this.stepThree.status = rowData.status;
    }
  }
});
