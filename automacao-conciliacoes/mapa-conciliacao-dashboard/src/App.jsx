import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert.jsx'
import { 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  RefreshCw, 
  FileText, 
  Calendar,
  TrendingUp,
  DollarSign,
  FileCheck,
  Clock
} from 'lucide-react'
import './App.css'

function App() {
  const [dados, setDados] = useState(null)
  const [carregando, setCarregando] = useState(true)
  const [ultimaAtualizacao, setUltimaAtualizacao] = useState(new Date())

  // Simula carregamento de dados do JSON
  useEffect(() => {
    carregarDados()
  }, [])

  const carregarDados = async () => {
    setCarregando(true)
    
    // Simula dados baseados na configuração
    const dadosSimulados = {
      timestamp_execucao: new Date().toISOString(),
      total_arquivos: 9,
      arquivos_encontrados: 0,
      arquivos_faltando: 9,
      resultados: [
        {
          nome_arquivo: "Rentabilidade_Carteira_A_20250606.xlsx",
          caminho_completo: "C:\\Conciliacoes\\Rentabilidade\\Carteira_A\\Rentabilidade_Carteira_A_20250606.xlsx",
          existe: false,
          criticidade: "alta",
          categoria: "rentabilidade",
          descricao: "Conciliação de rentabilidade da Carteira A"
        },
        {
          nome_arquivo: "Rentabilidade_Carteira_B_20250606.xlsx", 
          caminho_completo: "C:\\Conciliacoes\\Rentabilidade\\Carteira_B\\Rentabilidade_Carteira_B_20250606.xlsx",
          existe: false,
          criticidade: "alta",
          categoria: "rentabilidade",
          descricao: "Conciliação de rentabilidade da Carteira B"
        },
        {
          nome_arquivo: "Rentabilidade_Consolidada_20250606.xlsx",
          caminho_completo: "C:\\Conciliacoes\\Rentabilidade\\Consolidado\\Rentabilidade_Consolidada_20250606.xlsx",
          existe: false,
          criticidade: "critica",
          categoria: "rentabilidade",
          descricao: "Conciliação consolidada de rentabilidade"
        },
        {
          nome_arquivo: "IR_Retido_Fonte_20250606.xlsx",
          caminho_completo: "C:\\Conciliacoes\\Impostos\\IR\\IR_Retido_Fonte_20250606.xlsx",
          existe: false,
          criticidade: "alta",
          categoria: "impostos",
          descricao: "Conciliação de IR retido na fonte"
        },
        {
          nome_arquivo: "IOF_Operacoes_20250606.xlsx",
          caminho_completo: "C:\\Conciliacoes\\Impostos\\IOF\\IOF_Operacoes_20250606.xlsx",
          existe: false,
          criticidade: "media",
          categoria: "impostos",
          descricao: "Conciliação de IOF sobre operações"
        },
        {
          nome_arquivo: "PIS_COFINS_20250606.xlsx",
          caminho_completo: "C:\\Conciliacoes\\Impostos\\PIS_COFINS\\PIS_COFINS_20250606.xlsx",
          existe: false,
          criticidade: "media",
          categoria: "impostos",
          descricao: "Conciliação de PIS/COFINS"
        },
        {
          nome_arquivo: "Custodia_Titulos_20250606.xlsx",
          caminho_completo: "C:\\Conciliacoes\\Custodia\\Custodia_Titulos_20250606.xlsx",
          existe: false,
          criticidade: "media",
          categoria: "outras",
          descricao: "Conciliação de custódia de títulos"
        },
        {
          nome_arquivo: "Liquidacao_D0_20250606.xlsx",
          caminho_completo: "C:\\Conciliacoes\\Liquidacao\\Liquidacao_D0_20250606.xlsx",
          existe: false,
          criticidade: "alta",
          categoria: "outras",
          descricao: "Conciliação de liquidação D+0"
        },
        {
          nome_arquivo: "Fechamento_Dia_20250606.xlsx",
          caminho_completo: "C:\\Conciliacoes\\Fechamento\\Fechamento_Dia_20250606.xlsx",
          existe: false,
          criticidade: "critica",
          categoria: "outras",
          descricao: "Conciliação de fechamento do dia"
        }
      ]
    }
    
    setTimeout(() => {
      setDados(dadosSimulados)
      setCarregando(false)
      setUltimaAtualizacao(new Date())
    }, 1000)
  }

  const obterCorCriticidade = (criticidade) => {
    switch (criticidade) {
      case 'critica': return 'destructive'
      case 'alta': return 'destructive'
      case 'media': return 'secondary'
      default: return 'secondary'
    }
  }

  const obterIconeCategoria = (categoria) => {
    switch (categoria) {
      case 'rentabilidade': return <TrendingUp className="h-4 w-4" />
      case 'impostos': return <DollarSign className="h-4 w-4" />
      case 'outras': return <FileCheck className="h-4 w-4" />
      default: return <FileText className="h-4 w-4" />
    }
  }

  const agruparPorCategoria = (resultados) => {
    return resultados.reduce((acc, item) => {
      if (!acc[item.categoria]) {
        acc[item.categoria] = []
      }
      acc[item.categoria].push(item)
      return acc
    }, {})
  }

  const calcularTaxaSucesso = () => {
    if (!dados) return 0
    return dados.total_arquivos > 0 ? (dados.arquivos_encontrados / dados.total_arquivos) * 100 : 0
  }

  const obterProblemasCriticos = () => {
    if (!dados) return []
    return dados.resultados.filter(r => !r.existe && (r.criticidade === 'critica' || r.criticidade === 'alta'))
  }

  if (carregando) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
          <p className="text-lg font-medium text-gray-700">Carregando dados de conciliação...</p>
        </div>
      </div>
    )
  }

  const taxaSucesso = calcularTaxaSucesso()
  const problemasCriticos = obterProblemasCriticos()
  const categorias = agruparPorCategoria(dados.resultados)

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <FileText className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Dashboard de Conciliações</h1>
                <p className="text-sm text-gray-500">Galapagos DTVM - Monitoramento em Tempo Real</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-500">Última atualização</p>
                <p className="text-sm font-medium flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  {ultimaAtualizacao.toLocaleTimeString('pt-BR')}
                </p>
              </div>
              <Button onClick={carregarDados} variant="outline" size="sm">
                <RefreshCw className="h-4 w-4 mr-2" />
                Atualizar
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Alertas Críticos */}
        {problemasCriticos.length > 0 && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertTriangle className="h-4 w-4 text-red-600" />
            <AlertTitle className="text-red-800">Problemas Críticos Detectados</AlertTitle>
            <AlertDescription className="text-red-700">
              {problemasCriticos.length} arquivo(s) crítico(s) não encontrado(s). Ação imediata necessária.
            </AlertDescription>
          </Alert>
        )}

        {/* Cards de Estatísticas */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-r from-blue-500 to-blue-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total de Arquivos</CardTitle>
              <FileText className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dados.total_arquivos}</div>
              <p className="text-xs text-blue-100">Arquivos monitorados</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-green-500 to-green-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Encontrados</CardTitle>
              <CheckCircle className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dados.arquivos_encontrados}</div>
              <p className="text-xs text-green-100">Conciliações OK</p>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-r from-red-500 to-red-600 text-white">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Faltando</CardTitle>
              <XCircle className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dados.arquivos_faltando}</div>
              <p className="text-xs text-red-100">Requer atenção</p>
            </CardContent>
          </Card>

          <Card className={`bg-gradient-to-r ${taxaSucesso >= 90 ? 'from-green-500 to-green-600' : taxaSucesso >= 70 ? 'from-yellow-500 to-yellow-600' : 'from-red-500 to-red-600'} text-white`}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Taxa de Sucesso</CardTitle>
              <TrendingUp className="h-4 w-4" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{taxaSucesso.toFixed(1)}%</div>
              <Progress value={taxaSucesso} className="mt-2 bg-white/20" />
            </CardContent>
          </Card>
        </div>

        {/* Seções por Categoria */}
        {Object.entries(categorias).map(([categoria, arquivos]) => (
          <Card key={categoria} className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2 text-lg">
                {obterIconeCategoria(categoria)}
                <span className="capitalize">{categoria}</span>
                <Badge variant="outline">{arquivos.length} arquivos</Badge>
              </CardTitle>
              <CardDescription>
                {categoria === 'rentabilidade' && 'Conciliações de rentabilidade das carteiras'}
                {categoria === 'impostos' && 'Conciliações de impostos e tributos'}
                {categoria === 'outras' && 'Outras conciliações operacionais'}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4">
                {arquivos.map((arquivo, index) => (
                  <div key={index} className={`p-4 rounded-lg border-l-4 ${arquivo.existe ? 'border-l-green-500 bg-green-50' : 'border-l-red-500 bg-red-50'}`}>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          {arquivo.existe ? (
                            <CheckCircle className="h-5 w-5 text-green-600" />
                          ) : (
                            <XCircle className="h-5 w-5 text-red-600" />
                          )}
                          <h4 className="font-medium text-gray-900">{arquivo.nome_arquivo}</h4>
                          <Badge variant={obterCorCriticidade(arquivo.criticidade)} size="sm">
                            {arquivo.criticidade.toUpperCase()}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-1">{arquivo.descricao}</p>
                        <p className="text-xs text-gray-500 font-mono break-all">{arquivo.caminho_completo}</p>
                      </div>
                      <div className="ml-4">
                        <Badge variant={arquivo.existe ? 'default' : 'destructive'}>
                          {arquivo.existe ? 'Encontrado' : 'Não Encontrado'}
                        </Badge>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}

        {/* Footer */}
        <div className="text-center text-sm text-gray-500 mt-8">
          <p>Sistema Automatizado de Conciliações - Galapagos DTVM</p>
          <p>Última execução: {new Date(dados.timestamp_execucao).toLocaleString('pt-BR')}</p>
        </div>
      </div>
    </div>
  )
}

export default App

