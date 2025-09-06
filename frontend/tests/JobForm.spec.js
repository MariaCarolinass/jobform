import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import JobForm from '../src/components/JobForm.vue'

describe('JobForm', () => {
    it('tem campos obrigatórios e impede envio quando faltam', async () => {
        const wrapper = mount(JobForm)
        await wrapper.find('form').trigger('submit.prevent')
        
        expect(wrapper.vm.errors.nome).toBeDefined()
        expect(wrapper.vm.errors.email).toBeDefined()
        expect(wrapper.vm.errors.telefone).toBeDefined()
        expect(wrapper.vm.errors.cargo_desejado).toBeDefined()
        expect(wrapper.vm.errors.escolaridade).toBeDefined()
        expect(wrapper.vm.errors.arquivo).toBeDefined()
    })
})