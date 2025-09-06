<template>
    <form @submit.prevent="submit" enctype="multipart/form-data" novalidate>
        <div class="field">
            <label for="nome">Nome *</label>
            <input id="nome" v-model.trim="form.nome" type="text" />
            <div v-if="errors.nome" class="error">{{ errors.nome }}</div>
        </div>

        <div class="field">
            <label for="email">E-mail *</label>
            <input id="email" v-model.trim="form.email" type="email" />
            <div v-if="errors.email" class="error">{{ errors.email }}</div>
        </div>

        <div class="field">
            <label for="telefone">Telefone *</label>
            <input id="telefone" v-model.trim="form.telefone" type="text" placeholder="(xx) xxxxx-xxxx" />
            <div v-if="errors.telefone" class="error">{{ errors.telefone }}</div>
        </div>

        <div class="field">
            <label for="cargo">Cargo Desejado *</label>
            <input id="cargo" v-model.trim="form.cargo_desejado" type="text" />
            <div v-if="errors.cargo_desejado" class="error">{{ errors.cargo_desejado }}</div>
        </div>

        <div class="field">
            <label for="escolaridade">Escolaridade *</label>
            <select id="escolaridade" v-model="form.escolaridade">
                <option value="">-- selecione --</option>
                <option>Ensino Fundamental</option>
                <option>Ensino Médio</option>
                <option>Graduação</option>
                <option>Pós-graduação</option>
                <option>Mestrado</option>
                <option>Doutorado</option>
            </select>
            <div v-if="errors.escolaridade" class="error">{{ errors.escolaridade }}</div>
        </div>

        <div class="field">
            <label for="observacoes">Observações</label>
            <textarea id="observacoes" v-model="form.observacoes" rows="3"></textarea>
        </div>

        <div class="field">
            <label for="arquivo">Arquivo (doc, docx, pdf) * — máximo 1MB</label>
            <input id="arquivo" ref="file" type="file" @change="onFileChange" accept=".pdf,.doc,.docx" />
            <div v-if="errors.arquivo" class="error">{{ errors.arquivo }}</div>
            <div v-if="fileName" class="small">Arquivo selecionado: {{ fileName }}</div>
        </div>

        <div style="display:flex; gap:12px; align-items:center; margin-top:12px">
            <button :disabled="submitting">Enviar</button>
            <div class="small">{{ statusMessage }}</div>
        </div>
    </form>
</template>

<script>
    import api from '../services/api'

    const ALLOWED_EXT = ['pdf', 'doc', 'docx']
    const MAX_BYTES = 1 * 1024 * 1024

    export default {
        name: 'JobForm',
        data() {
            return {
                form: {
                    nome: '',
                    email: '',
                    telefone: '',
                    cargo_desejado: '',
                    escolaridade: '',
                    observacoes: ''
                },
                arquivo: null,
                fileName: '',
                errors: {},
                submitting: false,
                statusMessage: ''
            }
        },
        methods: {
            onFileChange(e) {
                this.errors.arquivo = null
                const file = e.target.files[0]
                if (!file) {
                    this.arquivo = null
                    this.fileName = ''
                    return
                }
                const ext = (file.name.split('.').pop() || '').toLowerCase()
                if (!ALLOWED_EXT.includes(ext)) {
                    this.errors.arquivo = 'Extensão não permitida. Apenas pdf, doc, docx.'
                    this.arquivo = null
                    this.fileName = ''
                    this.$refs.file.value = ''
                    return
                }
                if (file.size > MAX_BYTES) {
                    this.errors.arquivo = 'Arquivo excede 1MB.'
                    this.arquivo = null
                    this.fileName = ''
                    this.$refs.file.value = ''
                    return
                }
                this.arquivo = file
                this.fileName = file.name
            },
            validate() {
                this.errors = {}
                if (!this.form.nome || this.form.nome.length < 2) this.errors.nome = 'Nome inválido.'
                if (!this.form.email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(this.form.email)) this.errors.email = 'E-mail inválido.'
                if (!this.form.telefone || this.form.telefone.length < 6) this.errors.telefone = 'Telefone inválido.'
                if (!this.form.cargo_desejado) this.errors.cargo_desejado = 'Campo obrigatório.'
                if (!this.form.escolaridade) this.errors.escolaridade = 'Campo obrigatório.'
                if (!this.arquivo) this.errors.arquivo = 'Envie um arquivo válido (pdf, doc, docx) até 1MB.'

                return Object.keys(this.errors).length === 0
            },
            async submit() {
                if (!this.validate()) return
                this.submitting = true
                this.statusMessage = 'Enviando...'

                const formData = new FormData()
                formData.append('nome', this.form.nome)
                formData.append('email', this.form.email)
                formData.append('telefone', this.form.telefone)
                formData.append('cargo_desejado', this.form.cargo_desejado)
                formData.append('escolaridade', this.form.escolaridade)
                if (this.form.observacoes) formData.append('observacoes', this.form.observacoes)
                formData.append('arquivo', this.arquivo)

                try {
                    const resp = await api.post('/candidatos', formData, {
                        headers: { 'Content-Type': 'multipart/form-data' }
                    })

                    if (resp.data.email_status === "ok") {
                        this.statusMessage = "Enviado com sucesso!"
                    } else {
                        this.statusMessage = "Currículo salvo, mas houve erro ao enviar e-mail."
                    }
                    
                    this.form = { nome:'', email:'', telefone:'', cargo_desejado:'', escolaridade:'', observacoes:'' }
                    this.arquivo = null
                    this.fileName = ''
                    this.$refs.file.value = ''
                } catch (err) {
                    console.error(err)
                    if (err.response && err.response.data) {
                        this.statusMessage = 'Erro: ' + (err.response.data.detail || JSON.stringify(err.response.data))
                    }
                } finally {
                    this.submitting = false
                    setTimeout(() => (this.statusMessage = ''), 5000)
                }
            }
        }
    }
</script>

<style scoped>
</style>