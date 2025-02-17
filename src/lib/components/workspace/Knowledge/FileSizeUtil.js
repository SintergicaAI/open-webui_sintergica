export class FileSizeUtil {
    /**
     * Convierte un tamaño en bytes a un formato legible (KB, MB, GB).
     * @param {number} bytes - Tamaño en bytes.
     * @param {number} decimals - Número de decimales (opcional, por defecto 2).
     * @returns {string} - Tamaño formateado como string con unidad (KB, MB, etc.).
     */
    static formatSize(bytes, decimals = 2) {
        if (bytes === 0) return '0 Bytes';

        const k = 1024;
        const units = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));

        return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + units[i];
    }

    /**
     * Calcula el tamaño total de una lista de archivos.
     * @param {Array} files - Lista de archivos con su información (incluyendo `meta.size`).
     * @returns {number} - Tamaño total en bytes.
     */
    static getTotalSize(files) {
        if (!Array.isArray(files)) {
            throw new Error("El argumento proporcionado no es una lista válida de archivos.");
        }

        return files.reduce((totalSize, file) => {
            if (file.meta && typeof file.meta.size === 'number') {
                return totalSize + file.meta.size;
            }
            return totalSize;
        }, 0);
    }

    /**
     * Calcula el tamaño total de una lista de archivos y lo devuelve en un formato legible.
     * @param {Array} files - Lista de archivos con su información (incluyendo `meta.size`).
     * @param {number} decimals - Número de decimales para el formato (opcional, por defecto 2).
     * @returns {string} - Tamaño total formateado (e.g., "5.12 MB").
     */
    static getFormattedTotalSize(files, decimals = 2) {
        const totalSize = this.getTotalSize(files);
        return this.formatSize(totalSize, decimals);
    }
}